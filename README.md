# Vendor Management System
Vendor Management System API
Welcome to the Vendor Management System API, a Django project for managing vendors, purchase orders, and performance metrics.

# Project Overview
The Vendor Management System provides a set of RESTful APIs for user authentication, vendor management, purchase order creation, and performance metric tracking. It is designed to streamline the process of handling vendors and purchase orders.

# Features
  + User Signup and Login
  + Vendor Management
  + Purchase Order Creation and Management
  + Performance Metrics Tracking

# Project Structure
The project structure follows common Django conventions:
  * vendor-management-system/: Django project directory
    * vendor_management_system/: Django project folder
    * vendors/: Django app containing API views, serializers, and models
    * manage.py: Django management script
    * requirements.txt: Project dependencies
    * README.md: Project documentation

# Installation
1. Clone the repository:
    git clone https://github.com/nitishkumar149345/vendor_management_system.git

2. cd vendor_management_system
3. python -m venv env
4. env\bin\activate - for mac
   env\Scripts\activate - for windows
5. pip install -r requirements.txt
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver

# API Documentation
* The API will be accessible at http://127.0.0.1:8000/.
* Access the admin interface at http://127.0.0.1:8000/admin/
