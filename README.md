#  Parking Management System Using Django

A web-based application built with Django to manage parking entries, categories, charges, and vehicles. This system is designed to handle vehicle entries, exits, parking categories, manage users, and provide analytics like earnings and availability.

---
##  Features

- **User Authentication**  
  Secure login/logout system with password update functionality.

- **Dashboard Overview**  
  Visual summary of:
  - Parked & departed vehicles  
  - Total vehicle limit  
  - Earnings  
  - Active categories and records

- **Category Management**
  - Add/edit/delete vehicle parking categories
  - Activate/deactivate category
  - Pagination and search

- **Vehicle Entry Management**
  - Track entries and assign to category
  - Prevent over-parking using vehicle limit logic
  - Toggle vehicle status (parked/leaved)

- **Search System**
  - Smart multi-field search for both categories and vehicles

- **Account Settings**
  - Change password with validation

---

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default), easily switchable to MySQL/PostgreSQL
- **Auth System:** Django's built-in user authentication

---

python manage.py createsuperuser
6. Run the Server
bash
Copy
Edit
python manage.py runserver
Now open http://127.0.0.1:8000 in your browser.
