from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime
import os
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/internship_matching'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

mongo = PyMongo(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Homepage with welcome message and navigation"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration with profile creation"""
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        skills = request.form['skills'].split(',')
        interests = request.form['interests'].split(',')
        education = request.form['education']
        experience = request.form['experience']
        
        # Check if user already exists
        if mongo.db.students.find_one({'email': email}):
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create student profile
        student = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'full_name': full_name,
            'skills': [skill.strip() for skill in skills],
            'interests': [interest.strip() for interest in interests],
            'education': education,
            'experience': experience,
            'created_at': datetime.now()
        }
        
        mongo.db.students.insert_one(student)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login (students and admin)"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'admin':
            # Admin login
            admin = mongo.db.admins.find_one({'email': email})
            if admin and check_password_hash(admin['password'], password):
                session['user_id'] = str(admin['_id'])
                session['user_type'] = 'admin'
                session['username'] = admin['username']
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials!', 'error')
        else:
            # Student login
            student = mongo.db.students.find_one({'email': email})
            if student and check_password_hash(student['password'], password):
                session['user_id'] = str(student['_id'])
                session['user_type'] = 'student'
                session['username'] = student['username']
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard with matched internships"""
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    student = mongo.db.students.find_one({'_id': ObjectId(session['user_id'])})
    matched_internships = mongo.db.matches.find({'student_id': session['user_id']})
    
    # Get full internship details for matched internships
    internships = []
    for match in matched_internships:
        internship = mongo.db.internships.find_one({'_id': ObjectId(match['internship_id'])})
        if internship:
            internship['match_score'] = match['match_score']
            internship['match_reason'] = match['match_reason']
            internships.append(internship)
    
    return render_template('student_dashboard.html', student=student, internships=internships)

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard with internship management"""
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    internships = list(mongo.db.internships.find())
    students = list(mongo.db.students.find())
    matches = list(mongo.db.matches.find())
    
    return render_template('admin_dashboard.html', 
                         internships=internships, 
                         students=students, 
                         matches=matches)

@app.route('/admin/post_internship', methods=['GET', 'POST'])
def post_internship():
    """Admin posts new internship"""
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        requirements = request.form['requirements'].split(',')
        location = request.form['location']
        duration = request.form['duration']
        stipend = request.form['stipend']
        category = request.form['category']
        
        # Create internship
        internship = {
            'title': title,
            'company': company,
            'description': description,
            'requirements': [req.strip() for req in requirements],
            'location': location,
            'duration': duration,
            'stipend': stipend,
            'category': category,
            'posted_by': session['user_id'],
            'posted_at': datetime.now(),
            'status': 'active'
        }
        
        mongo.db.internships.insert_one(internship)
        flash('Internship posted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('post_internship.html')

@app.route('/admin/match_internships')
def match_internships():
    """Automated matching logic for internships to students"""
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    # Clear existing matches
    mongo.db.matches.delete_many({})
    
    students = list(mongo.db.students.find())
    internships = list(mongo.db.internships.find({'status': 'active'}))
    
    matches_created = 0
    
    for student in students:
        student_skills = set(skill.lower() for skill in student['skills'])
        student_interests = set(interest.lower() for interest in student['interests'])
        
        for internship in internships:
            # Calculate match score based on skills and requirements
            internship_requirements = set(req.lower() for req in internship['requirements'])
            
            # Skill matching
            skill_match = len(student_skills.intersection(internship_requirements))
            skill_score = (skill_match / len(internship_requirements)) * 50 if internship_requirements else 0
            
            # Interest matching (bonus points)
            interest_match = len(student_interests.intersection(internship_requirements))
            interest_score = interest_match * 10
            
            # Random factor for variety
            random_score = random.randint(0, 20)
            
            total_score = skill_score + interest_score + random_score
            
            # Only match if score is above threshold
            if total_score >= 30:
                match = {
                    'student_id': str(student['_id']),
                    'internship_id': str(internship['_id']),
                    'match_score': round(total_score, 2),
                    'match_reason': f"Skills: {skill_match}/{len(internship_requirements)}, Interests: {interest_match}, Random: {random_score}",
                    'matched_at': datetime.now()
                }
                mongo.db.matches.insert_one(match)
                matches_created += 1
    
    flash(f'Successfully created {matches_created} matches!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_students')
def view_students():
    """Admin views all student profiles"""
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    students = list(mongo.db.students.find())
    return render_template('view_students.html', students=students)

@app.route('/student/apply/<internship_id>', methods=['POST'])
def apply_internship(internship_id):
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    if 'resume' not in request.files:
        flash('No resume file part', 'error')
        return redirect(url_for('student_dashboard'))
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('student_dashboard'))
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{session['user_id']}_{internship_id}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Record application in DB
        application = {
            'student_id': session['user_id'],
            'internship_id': internship_id,
            'resume_path': filename,
            'applied_at': datetime.now()
        }
        mongo.db.applications.insert_one(application)

        # Dummy email sending (for demo/testing)
        print(f"[DUMMY EMAIL] Would send resume '{filename}' for student ID {session['user_id']} to dummy@example.com")
        flash('Application submitted and resume sent to company!', 'success')
    else:
        flash('Invalid file type. Please upload a PDF, DOC, or DOCX.', 'error')
    return redirect(url_for('student_dashboard'))

if __name__ == '__main__':
    # Create default admin account if not exists
    if not mongo.db.admins.find_one({'email': 'admin@internship.com'}):
        admin = {
            'username': 'admin',
            'email': 'admin@internship.com',
            'password': generate_password_hash('admin123'),
            'created_at': datetime.now()
        }
        mongo.db.admins.insert_one(admin)
        print("Default admin account created: admin@internship.com / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 