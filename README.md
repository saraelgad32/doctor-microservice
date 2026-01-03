# Doctor Microservice

A microservice-based clinic platform built with **Django** and **gRPC**, designed for managing doctor appointments and patient interactions.

## Repository Overview

This project allows users to:

- Register and login as patients.
- View doctor profiles and specialties.
- Book and manage appointments.
- Communicate with doctors through gRPC services.

### Main Folders & Files

- `config.py` → configuration settings  
- `doctor.proto` → gRPC service definition  
- `doctor_pb2.py` & `doctor_pb2_grpc.py` → gRPC generated code  
- `server.py` → gRPC server  
- `setup_database.sql` → initial database setup  
- `django/clinic_platform/` → main Django project  
  - `core/` → main app logic (models, views, URLs)  
  - `templates/` → HTML templates  
  - `static/` → CSS & JS files  

## Project Folder Structure

```project/
│ config.py
│ doctor.proto
│ doctor_pb2.py
│ doctor_pb2_grpc.py
│ requirements.txt
│ server.py
│ setup_database.sql
│ tutorial.txt
│
├─ django/
│ └─ clinic_platform/
│ ├─ manage.py
│ ├─ clinic_platform/
│ │ ├─ asgi.py
│ │ ├─ settings.py
│ │ ├─ urls.py
│ │ ├─ wsgi.py
│ │ └─ init.py
│ │
│ ├─ core/
│ │ ├─ admin.py
│ │ ├─ apps.py
│ │ ├─ models.py
│ │ ├─ views.py
│ │ ├─ urls.py
│ │ └─ init.py
│ │
│ ├─ migrations/
│ │ └─ 0001_initial.py
│ │
│ ├─ static/
│ │ ├─ script.js
│ │ └─ styles.css
│ │
│ └─ templates/
│ ├─ index.html
│ ├─ about.html
│ ├─ contact.html
│ ├─ dashboard.html
│ ├─ doctors.html
│ ├─ login.html
│ ├─ register.html
│ ├─ profile.html
│ ├─ reservation.html
│ └─ terms.html```

##HOW TO USE?
===============================================================
   ##CLINIQUE MEDICALE - INSTALLATION GUIDE
===============================================================

Hi! Follow these steps exactly to run the Clinique Médicale project on your computer.

There are 3 main parts to this project:
1. The Database (SQL Server)
2. The Microservice (Python Backend)
3. The Website (Django)

---------------------------------------------------------------
PHASE 1: INSTALL PREREQUISITES
---------------------------------------------------------------
Before starting, make sure you have these installed:
1. Python: https://www.python.org/downloads/
   (Make sure to check "Add Python to PATH" during installation)
2. SQL Server Express (The database engine)
3. SSMS (SQL Server Management Studio - to view the database)

---------------------------------------------------------------
PHASE 2: SETUP THE DATABASE
---------------------------------------------------------------
1. Open "SQL Server Management Studio" (SSMS).
2. Connect to your local server.
   IMPORTANT: Copy the "Server Name" from the connect box (e.g., LAPTOP-XYZ\SQLEXPRESS). 
   You will need this name in Phase 3.
3. In SSMS, go to File > Open > File...
4. Select the file "setup_database.sql" included in this project folder.
5. Click the "Execute" button (or press F5).
   -> This creates the "DoctorServiceDB" and fills it with doctor data.

---------------------------------------------------------------
PHASE 3: CONFIGURE THE PROJECT
---------------------------------------------------------------
1. Open the file "config.py" in this folder using a text editor (Notepad or VS Code).
2. Look for this line:
   'server': r'WALIDD\SQLEXPRESS'
3. Delete "WALIDD\SQLEXPRESS" and paste YOUR Server Name that you copied in Phase 2.
   Example: 'server': r'MY-LAPTOP\SQLEXPRESS'
4. Save the file.

---------------------------------------------------------------
PHASE 4: INSTALL PYTHON LIBRARIES
---------------------------------------------------------------
1. Open your terminal (Command Prompt or PowerShell).
2. Navigate to this project folder.
   (Tip: Right-click inside the folder and select "Open in Terminal").
3. Run this command to install the required tools:
   pip install -r requirements.txt

---------------------------------------------------------------
PHASE 5: RUN THE APP (THE FINAL STEP)
---------------------------------------------------------------
Because this is a microservice architecture, you need TWO terminals open.

TERMINAL 1 (The Microservice):
------------------------------
1. Open a terminal in the project folder.
2. Run this command:
   python server.py
3. You should see: "Microservice is running..."
   -> DO NOT CLOSE THIS WINDOW.

TERMINAL 2 (The Website):
-------------------------
1. Open a SECOND terminal in the project folder.
2. Run this command:
   cd django\clinic_platform
then this command :
   python manage.py runserver
3. You should see: "Starting development server at http://127.0.0.1:8000/"

---------------------------------------------------------------
HOW TO USE
---------------------------------------------------------------
Open your web browser (Chrome/Edge) and go to:
http://127.0.0.1:8000/

Login Credentials (if created):
Username: admin
Password: (The one you created, or create a new account via 'Register')

===============================================================
TROUBLESHOOTING
===============================================================
- Error: "Connection refused"
  Solution: Make sure Terminal 1 (server.py) is running.

- Error: "Login failed for user..."
  Solution: Check your config.py file. Your computer name might be different.

- Error: "Module not found"
  Solution: Run `pip install -r requirements.txt` again.
