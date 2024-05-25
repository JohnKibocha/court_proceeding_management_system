# Case Proceedings Management System

## Overview

The Case Proceedings Management System is a web-based software solution designed to streamline and automate the management of legal proceedings. It provides a centralized platform for legal practitioners to register cases, submit documents, track case progress, generate invoices, and facilitate communication between stakeholders.

## Screenshots

![case_view.png](static%2Fscreenshots%2Fcase_view.png)

![invoice_view.png](static%2Fscreenshots%2Finvoice_view.png)

![legal_document_view.png](static%2Fscreenshots%2Flegal_document_view.png)

![sample_invoice.png](static%2Fscreenshots%2Fsample_invoice.png)

![sample_legal_document.png](static%2Fscreenshots%2Fsample_legal_document.png)

![user_login.png](static%2Fscreenshots%2Fuser_login.png)


## Objectives

1. **Efficient Case Management**: Enable users' and clerks' registration, capture court proceedings, and track cases effectively.
2. **Invoice Generation**: Generate invoices for case payment automatically.
3. **User Access Control**: Implement user access control based on roles and permissions.
4. **Communication Tools**: Facilitate communication between legal practitioners, clients, and other stakeholders.
5. **Scalability and Flexibility**: Provide a scalable and flexible platform to adapt to the evolving needs of legal practices, enabling users to make payments seamlessly.

## Functionality

### System Administrators (Admin and Clerks)

- **User Management**: Admins can manage user accounts, including registration, approval, and access control.
- **Case Registration**: Admins can register new cases, assign case numbers, and allocate resources.
- **Document Management**: Upload, categorize, and manage case-related documents securely.
- **Invoice Generation**: Generate invoices based on predefined billing rules and case activities.

### Legal Practitioners/Lawyers

- **Case Management**: View assigned cases, update case status, and track case progress.
- **Document Submission**: Submit case-related documents securely and track document status.
- **Communication**: Communicate with clients, colleagues, and other stakeholders within the system.
- **Time Tracking**: Record billable hours and activities for accurate billing and invoicing.

### Clients/Participants

- **Case Monitoring**: Monitor the progress of their cases, view documents, and communicate with legal practitioners.
- **Invoice Access**: Access and download invoices for services rendered.
- **Appointment Scheduling**: Schedule appointments with legal practitioners for consultations and meetings.

## How to Run This Project

### Prerequisites
- Python 3.12.2 or higher
- Django 5.0.2 or compatible version

### Steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/your_project.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd your_project
   ```

3. **Create and Activate a Virtual Environment:**
   ```bash
   # Linux/MacOs
   python -m venv .venv
   source .venv/bin/activate   
   ```
   ```bash
    # Windows
    python -m venv .venv
   .venv\Scripts\activate      
   ```

4. **Upgrade pip and Install Dependencies:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application:**
   Open your web browser and visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

8. **Admin Panel:**
  - Access the admin panel by appending `/admin` to the URL.
  - Log in using the superuser credentials created earlier.

9. **Additional Configuration for Contact Us Page:**
  - Open `settings.py` file and provide your email and password:
    ```python
    EMAIL_HOST_USER = 'youremail@gmail.com'
    EMAIL_HOST_PASSWORD = 'your email password'
    EMAIL_RECEIVING_USER = 'youremail@gmail.com'
    ```
  - Ensure that you allow less secure apps in your Gmail settings by visiting [https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps)

## Contact Developer

For any inquiries or assistance regarding the Case Proceedings Management System, please contact the developer at [johnkibocha@outlook.com](mailto:johnkibocha@outlook.com).

## Drawbacks/Improvements

- **Enhanced User Authentication**: Implement stricter user authentication mechanisms, such as two-factor authentication, to enhance security.
- **Improved User Interface**: Enhance the user interface to improve usability and user experience.
- **Performance Optimization**: Optimize database queries and system processes for improved performance, especially with a large volume of data.
- **Documentation Enhancement**: Continuously update and enhance system documentation to provide comprehensive guidance for users and administrators.
