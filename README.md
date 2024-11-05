# 📚 Bookkeeping Application

A comprehensive bookkeeping system designed for tracking financial transactions, generating reports, and maintaining audit trails. The application features user authentication, account management, transaction recording, and is built with a modular architecture to support future integrations, including machine learning enhancements.

---

## 🚀 Table of Contents

- [📚 Bookkeeping Application](#-bookkeeping-application)
  - [🚀 Table of Contents](#-table-of-contents)
  - [🛠️ Setup Instructions](#️-setup-instructions)
    - [🔧 Prerequisites](#-prerequisites)
    - [📂 Directory Structure](#-directory-structure)
    - [📦 Installation](#-installation)
    - [🗃️ Database Initialization \& Upgrade](#️-database-initialization--upgrade)
      - [**1. Ensure the `data` Directory Exists**](#1-ensure-the-data-directory-exists)
      - [**2. Configure the Database URI**](#2-configure-the-database-uri)
      - [**3. Initialize Flask-Migrate**](#3-initialize-flask-migrate)
      - [**4. Create the Initial Migration**](#4-create-the-initial-migration)
      - [**5. Apply the Migration to the Database**](#5-apply-the-migration-to-the-database)
    - [👤 Creating a User for Authentication](#-creating-a-user-for-authentication)
      - [**1. Activate the Virtual Environment**](#1-activate-the-virtual-environment)
      - [**2. Launch the Flask Shell**](#2-launch-the-flask-shell)
      - [**3. Import Necessary Modules**](#3-import-necessary-modules)
      - [**4. Create a New User**](#4-create-a-new-user)
      - [**5. Add and Commit the User to the Database**](#5-add-and-commit-the-user-to-the-database)
      - [**6. Verify User Creation**](#6-verify-user-creation)
      - [**7. Exit the Flask Shell**](#7-exit-the-flask-shell)
  - [🧪 Running Tests with Pytest](#-running-tests-with-pytest)
    - [**1. Activate the Virtual Environment**](#1-activate-the-virtual-environment-1)
    - [**2. Run Pytest**](#2-run-pytest)
  - [🏃 Running the Flask Application](#-running-the-flask-application)
    - [**1. Activate the Virtual Environment**](#1-activate-the-virtual-environment-2)
    - [**2. Set Environment Variables**](#2-set-environment-variables)
    - [**3. Run the Flask Development Server**](#3-run-the-flask-development-server)
    - [🔗 Accessing the Application](#-accessing-the-application)
  - [🖌️ User Interface Overview](#️-user-interface-overview)
    - [📋 Available Routes](#-available-routes)
    - [🔒 Authentication Flow](#-authentication-flow)
    - [📊 Managing Accounts](#-managing-accounts)
    - [💰 Recording Transactions](#-recording-transactions)
    - [🔄 Logging Out](#-logging-out)
  - [✅ Final Checklist](#-final-checklist)
  - [ℹ️ Additional Resources](#ℹ️-additional-resources)
  - [💡 Tips \& Best Practices](#-tips--best-practices)

---

## 🛠️ Setup Instructions

### 🔧 Prerequisites

Ensure you have the following installed on your system:

- **Python 3.13.0**: Download and install from [Python's official website](https://www.python.org/downloads/).
- **Virtual Environment** (`venv`): Comes bundled with Python 3. Ensure it's available in your Python installation.
- **Git** (optional): For version control and cloning repositories. Download from [Git's official website](https://git-scm.com/downloads).

### 📂 Directory Structure

Ensure your project has the following structure:

```
bookkeeping/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── account_form.html
│   │   ├── account_list.html
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── transaction_form.html
│   │   └── transaction_list.html
│   └── views/
│       ├── __init__.py
│       ├── accounts.py
│       ├── auth.py
│       ├── main.py
│       └── transactions.py
├── modules/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── account_form.py
│   │   ├── login_form.py
│   │   └── transaction_form.py
│   └── models/
│       ├── __init__.py
│       ├── account.py
│       ├── transaction.py
│       └── user.py
├── migrations/
│   ├── env.py
│   ├── README
│   └── versions/
│       └── e70c7b1df6a5_initial_migration.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   └── test_views.py
├── data/
│   └── app.db
├── config.py
├── requirements.txt
└── README.md
```

### 📦 Installation

1. **Clone the Repository** (if using Git):

    ```bash
    git clone https://github.com/yourusername/bookkeeping.git
    cd bookkeeping
    ```

2. **Create a Virtual Environment**:

    ```bash
    python -m venv .venv
    ```

3. **Activate the Virtual Environment**:

    - **On Unix/Linux/macOS or Git Bash:**

        ```bash
        source .venv/Scripts/activate
        ```

    - **On Windows (Command Prompt):**

        ```cmd
        .venv\Scripts\activate
        ```

    - **On Windows (PowerShell):**

        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```

4. **Install Required Packages**:

    Ensure your `requirements.txt` is up-to-date. If not, create one with the necessary dependencies:

    ```bash
    pip install Flask Flask-WTF Flask-Login Flask-Migrate Flask-SQLAlchemy pytest werkzeug
    pip freeze > requirements.txt
    ```

    Then, install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### 🗃️ Database Initialization & Upgrade

Follow these steps to initialize and upgrade your database using Flask-Migrate.

#### **1. Ensure the `data` Directory Exists**

SQLite requires the directory specified in the `SQLALCHEMY_DATABASE_URI` to exist.

```bash
mkdir data
```

*If the `data` directory already exists, you'll receive a message indicating so.*

#### **2. Configure the Database URI**

Ensure your `config.py` uses an absolute path for the database URI.

```python
# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    
    # Generate absolute path for the database
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory DB for testing
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
```

#### **3. Initialize Flask-Migrate**

If you haven't already initialized migrations, run:

```bash
flask db init
```

*Note: If the `migrations` directory already exists, you'll see a warning. You can safely proceed if migrations have been previously initialized.*

#### **4. Create the Initial Migration**

Generate the migration scripts based on your models.

```bash
flask db migrate -m "Initial migration."
```

**Expected Output:**

```plaintext
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'accounts'
INFO  [alembic.autogenerate.compare] Detected added table 'transactions'
Generating /path/to/migrations/versions/e70c7b1df6a5_initial_migration.py ... done
```

#### **5. Apply the Migration to the Database**

Execute the migration to create the database schema.

```bash
flask db upgrade
```

**Expected Output:**

```plaintext
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade e70c7b1df6a5 -> e70c7b1df6a5_initial_migration, Initial migration.
```

### 👤 Creating a User for Authentication

To authenticate users in your application, create at least one user using the Flask shell.

#### **1. Activate the Virtual Environment**

Ensure your virtual environment is active.

- **On Unix/Linux/macOS or Git Bash:**

    ```bash
    source .venv/Scripts/activate
    ```

- **On Windows (Command Prompt):**

    ```cmd
    .venv\Scripts\activate
    ```

- **On Windows (PowerShell):**

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

#### **2. Launch the Flask Shell**

Start the Flask interactive shell.

```bash
flask shell
```

**Expected Output:**

```plaintext
Python 3.13.0 (tags/v3.13.0:60403a5, Oct  7 2024, 09:38:07) [MSC v.1941 64 bit (AMD64)] on win32
App: app
Instance: C:\Users\khali\OneDrive - Khalid Taha 7865\my_code_collection\bookkeeping\instance
>>> 
```

#### **3. Import Necessary Modules**

Within the Flask shell, import the `User` model, the `db` instance, and the `generate_password_hash` function.

```python
from modules.models.user import User
from modules.database.db import db
from werkzeug.security import generate_password_hash
```

#### **4. Create a New User**

Instantiate a new user with a username, a hashed password, and a role.

```python
# Replace 'admin' and 'securepassword123' with your desired credentials
new_user = User(
    username='admin',
    password_hash=generate_password_hash('securepassword123'),
    role='Admin'
)
```

#### **5. Add and Commit the User to the Database**

Add the new user to the session and commit the transaction.

```python
db.session.add(new_user)
db.session.commit()
```

#### **6. Verify User Creation**

Ensure the user has been successfully added.

```python
created_user = User.query.filter_by(username='admin').first()
print(created_user)
```

**Expected Output:**

```plaintext
<User admin>
```

*(This confirms that the user `admin` exists in the database.)*

#### **7. Exit the Flask Shell**

Close the interactive shell.

```python
exit()
```

---

## 🧪 Running Tests with Pytest

Ensure your application is correctly set up by running your test suite.

### **1. Activate the Virtual Environment**

Ensure your virtual environment is active.

- **On Unix/Linux/macOS or Git Bash:**

    ```bash
    source .venv/Scripts/activate
    ```

- **On Windows (Command Prompt):**

    ```cmd
    .venv\Scripts\activate
    ```

- **On Windows (PowerShell):**

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

### **2. Run Pytest**

Execute the tests using `pytest`.

```bash
pytest
```

**Expected Output:**

```plaintext
================================= test session starts =================================
platform win32 -- Python 3.13.0, pytest-8.3.3, pluggy-1.5.0
rootdir: C:\Users\khali\OneDrive - Khalid Taha 7865\my_code_collection\bookkeeping
collected 2 items

tests\test_models.py .                                                [ 50%]
tests\test_views.py .                                                 [100%]

================================== 2 passed in 0.77s ================================
```

*If tests fail, review the error messages for troubleshooting.*

---

## 🏃 Running the Flask Application

With the database initialized and a user created, you can now run your Flask application.

### **1. Activate the Virtual Environment**

Ensure your virtual environment is active.

- **On Unix/Linux/macOS or Git Bash:**

    ```bash
    source .venv/Scripts/activate
    ```

- **On Windows (Command Prompt):**

    ```cmd
    .venv\Scripts\activate
    ```

- **On Windows (PowerShell):**

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

### **2. Set Environment Variables**

Configure environment variables based on your operating system.

- **Using Git Bash or Unix Shell:**

    ```bash
    export FLASK_APP=app/main.py
    export FLASK_ENV=development
    ```

- **Using Windows Command Prompt:**

    ```cmd
    set FLASK_APP=app/main.py
    set FLASK_ENV=development
    ```

- **Using Windows PowerShell:**

    ```powershell
    $env:FLASK_APP = "app/main.py"
    $env:FLASK_ENV = "development"
    ```

### **3. Run the Flask Development Server**

Start the Flask server.

```bash
flask run
```

**Expected Output:**

```plaintext
 * Serving Flask app 'app/main.py'
 * Environment: development
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

### 🔗 Accessing the Application

1. **Open Your Web Browser.**

2. **Navigate to the Login Page:**

    ```
    http://localhost:5000/auth/login
    ```

3. **Login Using the Created User:**

    - **Username:** `admin`
    - **Password:** `securepassword123`

4. **Test Application Functionality:**

    - **Create Accounts:**
        - Navigate to `http://localhost:5000/accounts/new`.
        - Fill out the form and submit.
    
    - **List Accounts:**
        - Navigate to `http://localhost:5000/accounts/` or use the link provided in the navigation bar.
    
    - **Create Transactions:**
        - Navigate to `http://localhost:5000/transactions/new`.
        - Fill out the form and submit.
    
    - **List Transactions:**
        - Navigate to `http://localhost:5000/transactions/` or use the link provided in the navigation bar.
    
    - **Logout:**
        - Click on the "Logout" link available in the navigation bar or navigate to `http://localhost:5000/auth/logout`.

---

## 🖌️ User Interface Overview

### 📋 Available Routes

- **Home Page:** `http://localhost:5000/`
- **Login:** `http://localhost:5000/auth/login`
- **Logout:** `http://localhost:5000/auth/logout`
- **Create Account:** `http://localhost:5000/accounts/new`
- **List Accounts:** `http://localhost:5000/accounts/`
- **Create Transaction:** `http://localhost:5000/transactions/new`
- **List Transactions:** `http://localhost:5000/transactions/`

### 🔒 Authentication Flow

1. **Access Login Page:**  
   Navigate to `/auth/login` to access the login form.

2. **Submit Credentials:**  
   Enter your username and password. Upon successful authentication, you'll be redirected to the Home page.

3. **Access Protected Routes:**  
   Only authenticated users can access account and transaction management routes.

4. **Logout:**  
   Click on the "Logout" link to end your session.

### 📊 Managing Accounts

1. **Create a New Account:**
    - Navigate to `/accounts/new`.
    - Fill out the form with the account name and type.
    - Submit to create the account.
    - **Note:** Account names must be unique. Attempting to create a duplicate account will display an error message.

2. **List Existing Accounts:**
    - Navigate to `/accounts/`.
    - View a list of all created accounts with their names and types.

### 💰 Recording Transactions

1. **Create a New Transaction:**
    - Navigate to `/transactions/new`.
    - Fill out the form with the transaction date, amount, description, debit account, and credit account.
    - Submit to record the transaction.
    - **Note:** Ensure that the selected debit and credit accounts exist.

2. **List Existing Transactions:**
    - Navigate to `/transactions/`.
    - View a list of all recorded transactions with their descriptions, amounts, and dates.

### 🔄 Logging Out

- **Logout:**  
  Click on the "Logout" link available in the navigation bar or navigate to `/auth/logout` to end your session.

---

## ✅ Final Checklist

Before considering the setup complete, ensure the following:

1. **Directory Structure:**
    - All necessary directories and `__init__.py` files exist.
    
2. **Blueprints:**
    - Blueprints (`auth`, `accounts`, `transactions`, `main`) are correctly defined and registered in `app/__init__.py`.
    
3. **Flask Extensions:**
    - All extensions (`SQLAlchemy`, `Flask-Migrate`, `Flask-Login`) are initialized before registering blueprints.
    
4. **Configuration:**
    - `config.py` has the correct `SQLALCHEMY_DATABASE_URI` and `SECRET_KEY`.
    - Environment variables (`FLASK_APP`, `FLASK_ENV`) are set appropriately.
    
5. **Database:**
    - Flask-Migrate is initialized.
    - Initial migration has been created and applied.
    - Database tables reflect your models.
    
6. **User Authentication:**
    - At least one user (`admin`) is created for logging in.
    - Authentication routes (`/auth/login`, `/auth/logout`) are accessible and functional.
    
7. **Templates:**
    - All necessary HTML templates (e.g., `login.html`, `account_form.html`, `transaction_form.html`) are present in `app/templates/`.
    - Templates correctly extend a base template (`base.html`) if used.
    
8. **Testing:**
    - `conftest.py` is correctly set up with necessary fixtures.
    - Test files correctly utilize fixtures and import necessary modules.
    - All tests pass when running `pytest`.
    
9. **Dependencies:**
    - All required packages are installed in the virtual environment (`pip install -r requirements.txt`).
    
10. **Static Files:**
    - CSS styles are correctly linked and applied. Verify by checking the UI in your browser.

---

## ℹ️ Additional Resources

- **Flask Documentation:** [https://flask.palletsprojects.com/en/2.3.x/](https://flask.palletsprojects.com/en/2.3.x/)
- **Flask-Migrate Documentation:** [https://flask-migrate.readthedocs.io/en/latest/](https://flask-migrate.readthedocs.io/en/latest/)
- **Flask-Login Documentation:** [https://flask-login.readthedocs.io/en/latest/](https://flask-login.readthedocs.io/en/latest/)
- **Pytest Documentation:** [https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/)
- **Understanding Circular Imports in Python:** [https://realpython.com/python-import/#circular-imports](https://realpython.com/python-import/#circular-imports)

---

## 💡 Tips & Best Practices

1. **Environment Variables:**
    - Use environment variables to manage sensitive data like `SECRET_KEY`. Consider using packages like `python-dotenv` to manage these variables easily.
    
2. **Error Handling:**
    - Ensure that all forms and routes handle errors gracefully, providing meaningful feedback to users.
    
3. **User Roles & Permissions:**
    - Expand the `User` model to include roles and permissions, enhancing security and access control.
    
4. **Styling & Responsiveness:**
    - Enhance the UI by integrating CSS frameworks like [Bootstrap](https://getbootstrap.com/) for a more polished and responsive design.
    
5. **API Development:**
    - Consider developing RESTful APIs for your application, enabling integration with other services or frontend frameworks.
    
6. **Continuous Integration:**
    - Set up CI/CD pipelines using tools like GitHub Actions or Travis CI to automate testing and deployment processes.
    
7. **Logging & Monitoring:**
    - Implement logging to track application behavior and errors. Tools like [Flask-Logging](https://flask.palletsprojects.com/en/2.3.x/logging/) can be beneficial.
    
8. **Documentation:**
    - Maintain comprehensive documentation for your codebase, aiding future development and collaboration.

---
