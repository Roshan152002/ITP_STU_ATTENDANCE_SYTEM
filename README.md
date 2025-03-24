# Student Attendance and Test Management System

## 📌 Project Overview
The **Student Attendance and Test Management System** is a Django-based web application that facilitates the management of student attendance and test records. The system allows teachers to mark attendance, manage student records, and generate reports efficiently.

## 🚀 Features
- **User Authentication**: Secure login for students, teachers, and admins.
- **Student Management**: Enroll students, update details, and view attendance records.
- **Teacher Management**: Assign subjects, mark attendance, and manage test scores.
- **Attendance System**: Track attendance for each student based on subjects.
- **Test Management**: Store and retrieve student test results.
- **Dashboard**: View reports, analytics, and system status.

---
## 🛠️ Installation Steps
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Django
- SQLite (or any other database of choice)

### Steps to Run the Project
1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd student-attendance-management
   ```
2. **Create a Virtual Environment**:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```
3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run Migrations**:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a Superuser**:
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the Server**:
   ```sh
   python manage.py runserver
   ```
7. **Access the Application**:
   Open your browser and go to `http://127.0.0.1:8000/`

---
## 📂 Project Structure
```
📦 student-attendance-management
├── 📂 attendance
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│
├── 📂 ITP_STU_ATTENDANCE
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── studentViews.py
│   ├── teacherViews.py
│   ├── adminViews.py
│
├── 📂 media/profile_pics
├── 📂 static
├── 📂 templates
│   ├── admin/
│   ├── include/
│   ├── student/
│   ├── teacher/
│   ├── base.html
│
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
```
---
## 📅 Development Timeline

### **Week 1: Project Setup & Authentication**
✅ Setup Django project and virtual environment  
✅ Create user authentication system (Login, Registration)  
✅ Implement student and teacher user roles  
✅ Configure database and migrations  

### **Week 2: Models & Views**
✅ Define models for Student, Teacher, Attendance, and Test Management  
✅ Create Teacher and Student Views  
✅ Implement attendance system logic  

### **Week 3: Templates & User Interface**
✅ Design base template (dashboard)  
✅ Develop student and teacher dashboards  
✅ Implement forms for attendance marking  
✅ Implement student profile management  

### **Week 4: Finalizing & Deployment**
✅ Implement test result management  
✅ Optimize queries for performance  
✅ Final testing and debugging  
✅ Deploy on a hosting platform  

---
## 📌 Contribution
Want to contribute? Follow these steps:
1. Fork the repository
2. Create a new branch (`feature-xyz`)
3. Commit your changes
4. Push the branch and create a Pull Request

---
## 📞 Support
For queries or suggestions, feel free to reach out. ✨

