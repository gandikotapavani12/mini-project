# Profile-Based Internship Matching System

A comprehensive web application that intelligently matches students with internship opportunities based on their skills, interests, and career goals. Built with Flask, MongoDB, and Tailwind CSS.

## 🎯 Project Overview

This system provides a platform where:
- **Students** can create detailed profiles with their skills, interests, education, and experience
- **Admins** can post internship opportunities with specific requirements
- **AI-powered matching algorithm** automatically connects students with relevant internships
- **Beautiful UI** with modern design and intuitive user experience

## ✨ Features

### For Students
- 📝 **Profile Creation**: Build comprehensive profiles with skills, interests, education, and experience
- 🎯 **Smart Matching**: Get matched with internships based on your profile
- 📊 **Match Scores**: See why each internship is a good fit with detailed match explanations
- 💼 **Apply to Matches**: Easy application process for matched opportunities

### For Admins
- 🏢 **Internship Management**: Post and manage internship opportunities
- 👥 **Student Overview**: View all student profiles and their details
- 🤖 **Matching Algorithm**: Run intelligent matching between students and internships
- 📈 **Analytics Dashboard**: Monitor system statistics and match rates

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB
- **Frontend**: HTML + Tailwind CSS
- **Authentication**: Session-based with password hashing
- **Matching Algorithm**: Custom logic with skill/interest matching + randomization

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB (local or cloud instance)
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd internship-matching-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: MongoDB Setup
1. Install MongoDB locally or use MongoDB Atlas (cloud)
2. Create a database named `internship_matching`
3. Update the MongoDB connection string in `app.py` if needed:
   ```python
   app.config['MONGO_URI'] = 'mongodb://localhost:27017/internship_matching'
   ```

### Step 4: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 👤 Default Admin Account

The system creates a default admin account automatically:
- **Email**: admin@internship.com
- **Password**: admin123

## 📋 Usage Guide

### For Students

1. **Register**: Visit the homepage and click "Register"
2. **Create Profile**: Fill in your details including:
   - Basic information (name, email, username)
   - Technical skills (Python, JavaScript, React, etc.)
   - Career interests (Web Development, AI/ML, Data Science, etc.)
   - Education background
   - Experience and projects
3. **Login**: Use your credentials to access your dashboard
4. **View Matches**: See internships matched to your profile with match scores
5. **Apply**: Click "Apply Now" on internships you're interested in

### For Admins

1. **Login**: Use the default admin credentials or create a new admin account
2. **Post Internships**: Click "Post New Internship" and fill in:
   - Basic information (title, company, description)
   - Required skills and qualifications
   - Location and duration
   - Compensation and category
3. **Run Matching**: Click "Run Matching Algorithm" to match students with internships
4. **View Students**: Browse all student profiles and their details
5. **Monitor**: Check dashboard statistics and recent matches

## 🧠 Matching Algorithm

The system uses a sophisticated matching algorithm that considers:

1. **Skill Matching** (50% weight): Compares student skills with internship requirements
2. **Interest Matching** (bonus points): Aligns student interests with internship needs
3. **Randomization** (0-20 points): Adds variety and prevents bias
4. **Threshold**: Only matches with scores ≥30% are created

### Match Score Calculation
```
Total Score = Skill Score + Interest Score + Random Score
Skill Score = (Matching Skills / Total Required Skills) × 50
Interest Score = Matching Interests × 10
Random Score = Random(0-20)
```

## 📁 Project Structure

```
internship-matching-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Homepage
    ├── register.html     # Student registration
    ├── login.html        # Login page
    ├── student_dashboard.html    # Student dashboard
    ├── admin_dashboard.html      # Admin dashboard
    ├── post_internship.html      # Internship posting form
    └── view_students.html        # Student profiles view
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional design with Tailwind CSS
- **Color-coded Sections**: Different colors for different types of information
- **Interactive Elements**: Hover effects, transitions, and animations
- **User-friendly Forms**: Clear prompts and helpful tips
- **Visual Feedback**: Success/error messages and loading states

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Secure user sessions
- **Input Validation**: Form validation and sanitization
- **Access Control**: Role-based access (student vs admin)

## 🚀 Future Enhancements

- [ ] Email notifications for new matches
- [ ] Advanced filtering and search
- [ ] Resume upload functionality
- [ ] Interview scheduling system
- [ ] Company profiles and branding
- [ ] Analytics and reporting
- [ ] Mobile app development
- [ ] API endpoints for external integrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support or questions, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for connecting students with their dream internships!** 