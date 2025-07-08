## 🔐 Hide & Seek: An Image-Based Steganography System

A secure, intelligent, and user-friendly Django web application for Encoding and Decoding hidden messages within images using LSB (Least Significant Bit) Substitution, enhanced with AI-based Message Validation using Constraint Satisfaction Problem (CSP) techniques.


------------------------------------------------------------------------------------------------------------------------
### 📝 Project Description

Hide & Seek is a web-based steganography system that allows users to securely hide secret text messages inside images and extract them later. 
With added AI-based Message Validator, the system ensures messages are safe, non-offensive, and format-compliant before they are hidden inside images.


------------------------------------------------------------------------------------------------------------------------
### 🔍 Key Features

    •	✅ Encode messages into images

    •	🔓 Decode hidden messages from images

    •	🛡️ AI-based Message Validation using CSP constraints:

              o	Filters banned words, emojis, all caps, offensive content

    •	📂 Two types of gallery: Encoded & To-Encode Images

    •	🔐 Secure user login, profile photo display, and password change

    •	👥 User-based access control for added privacy

    •	🎨 Aesthetic and intuitive UI with smooth navigation

    •	📥 Image download option for encoded images



------------------------------------------------------------------------------------------------------------------------
### 👩‍💻 Contributors & Roles


👤 Akhi Moon Jahan (ID: C223202)

    •	📝 Designed the Sign Up & Login system with user authentication

    •	👤 Created the Profile Display and Error Pages for better UX

    •	🖼️ Developed the Encoded Images Gallery and To-Encode Image Gallery 

    •	🔍 Contributed to the design and testing of the AI-based Message Validator module

    •	🎨 Styled and refined many UI components for consistency and responsiveness



👤 Fayeza Afrah Hissan (ID: C223206)

    •	🏠 Designed the Home/Index page with navigation, structure, and layout

    •	🧬 Developed the Encoding and Decoding logic and UI

    •	💡 Designed and implemented the About page showcasing the project features and concepts

    •	🧠 Built the AI-based Message Validation feature using CSP

    •	📋 Helped design rules and constraints for secure message validation



------------------------------------------------------------------------------------------------------------------------
### ⚙️ Tech Stack

    •	Backend: Django (Python)

    •	Frontend: HTML, CSS, JavaScript

    •	AI/Validation: Python CSP logic, profanity & dictionary filtering

    •	Database: SQLite3 (default for Django)

    •	Deployment: Run locally via manage.py runserver (run from inside the hideseek folder using PowerShell)



------------------------------------------------------------------------------------------------------------------------
### 🚀 Steps to Run the Project

    📦 1. Install Required Tools

        Make sure you have these installed:

            •	Python 3.10 or higher (e.g., Python 3.13)

            •	Django 5.2.3

            •	pip (Python package manager)
            
            •	Git

            •	virtualenv (optional but recommended)

    🛠️ 2. Clone the Project Repository

            ```bash
            
            git clone https://github.com/FAH-works/Hide-Seek.git
            
            cd Hide-Seek


    📁 3. Set Up a Virtual Environment (Optional but recommended)

            python -m venv .venv

            .venv\Scripts\activate   


    📚 4. Install Required Packages

            pip install -r requirements.txt

        Also download the NLTK English word list:

            import nltk

            nltk.download('words')


    ⚙️ 5. Run Migrations

            python manage.py makemigrations

            python manage.py migrate


    👤 6. (Optional) Create a Superuser

            python manage.py createsuperuser


    ▶️ 7. Start the Django Server

            python manage.py runserver

        Visit the site in your browser at:

            http://127.0.0.1:8000/



------------------------------------------------------------------------------------------------------------------------
### 📄 License

This project is open-source and developed for academic purposes.

All rights reserved ©️ 2025 –Akhi Moon Jahan & Fayeza Afrah Hissan

