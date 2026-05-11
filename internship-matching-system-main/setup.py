#!/usr/bin/env python3
"""
Setup script for Profile-Based Internship Matching System
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        return False

def check_mongodb():
    """Check if MongoDB is accessible"""
    print("\n🗄️  Checking MongoDB connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print("❌ MongoDB connection failed")
        print("Please ensure MongoDB is running on localhost:27017")
        print("Or update the connection string in app.py")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ['logs', 'uploads']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Profile-Based Internship Matching System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check MongoDB
    if not check_mongodb():
        print("\n⚠️  MongoDB setup required:")
        print("1. Install MongoDB locally or use MongoDB Atlas")
        print("2. Ensure MongoDB is running")
        print("3. Update connection string in app.py if needed")
    
    # Create directories
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the application: python app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Login as admin: admin@internship.com / admin123")
    print("4. Register student accounts and post internships")
    print("5. Run the matching algorithm to see matches")

if __name__ == "__main__":
    main() 