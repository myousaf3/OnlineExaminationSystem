## Online Examination System

Online Examination System is a web application built using Django that allows educational institutions to offer online exams to their students. The system provides an easy-to-use interface for creating and managing exams, as well as tools for grading and analyzing student performance.
Features

    User authentication and authorization
    Admin dashboard for managing exams, questions, and grading
    Ability to create multiple choice and true/false questions
    Timer-based exam submissions
    Grading and analysis tools for instructors

## Installation

    - Clone the repository: git clone https://github.com/your-github-username/online-examination-system.git
    - Navigate into the project directory: cd online-examination-system
    - Create a virtual environment: python -m venv env
    - Activate the virtual environment: source env/bin/activate (Linux/Mac) or env\Scripts\activate (Windows)
    - Install dependencies: pip install -r requirements.txt
    - Run migrations: python manage.py migrate
    - Create a superuser account: python manage.py createsuperuser
    - Start the development server: python manage.py runserver

## Usage

After completing the installation steps, you can access the Online Examination System by navigating to http://localhost:8000 in your web browser.
Creating an Exam

As an admin user, you can create new exams by navigating to the Admin Dashboard (http://localhost:8000/admin) and clicking on the "Add" button next to the "Exams" section. You will be prompted to enter basic information about the exam, such as its name and duration.

Once you have created an exam, you can add questions by clicking on the "Add Question" button within the exam details screen. You can create multiple choice or true/false questions, and specify the correct answer for each question.
Taking an Exam

Students can access exams by navigating to http://localhost:8000/exams and selecting the exam they wish to take. Exams are timed, and students must complete the exam within the allotted time period.
Grading an Exam

As an admin user, you can view and grade completed exams by navigating to the Admin Dashboard and clicking on the "Exam Results" section. From there, you can view individual student submissions and assign grades based on their performance.
License

This project is licensed under the MIT License. See the LICENSE file for details.
