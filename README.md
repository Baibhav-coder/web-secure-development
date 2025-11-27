# 1. 💪 SecureFit – Secure Web Application Development Project
SecureFit: A Django-based gym membership application that I created to demonstrate three typical web-security vulnerabilities and solutions to fix them using sound coding principles.

The project includes:
- A visibly weak version.
- A fully secured version
- A well defined commit history demonstrating enhancement and safety enhancements.
- A video of the findings and countermeasures.

This README provides an overview of the whole module according to the module requirements.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 2. 📌 Features & Security Objectives

Application Features

- Signup: User can use their information to sign up.
- Login/Logout: This is because users are able to log in and out of their accounts.
- Membership Plan Listing: This is where the members can see the membership plans.
- Membership Purchase Process: It has a step by step process of purchasing a plan.
- Check Personal Purchase History: This option is provided to view the list of all the previous purchases.
- Get Purchase Detail (Secured after fix):now, users can dig the details of each purchase, as we have already fixed the security issue.
- CRUD Operations: The admins are able to create, read, update and delete contents through the administration panel.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 3. 🪪 Security Focus

| Vulnerability                | Description                                                                         | Status            |
| ---------------------------- | ----------------------------------------------------------------------------------- | ----------------- |
| **SQL Injection**            | In my project, I had to use a raw SQL query of the login, which directly accepted user input.   | ❌ Discovered → ✔ Mitigated |
| **IDOR**                     | Anyone was able to just change the purchase ID in the URL and view the purchase of other users. | ❌ Discovered → ✔ Mitigated |
| **Unsafe Cookie Settings** | JavaScript could be used to attack cookies in cross-site attacks.| ❌ Discovered → ✔ Mitigated |

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4. 📁 Project Structure

<img width="517" height="682" alt="image" src="https://github.com/user-attachments/assets/41e1ea9e-8fed-4036-9101-b57c18466261" />

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5. 🛠️ Setup & Installation Instructions

✅ 1. Clone the Repository

-git clone https://github.com/Baibhav-coder/web-secure-development.git

-cd web-secure-development

✅ 2. Create and Activate a Virtual Environment

For Windows (PowerShell)

-python -m venv venv

-venv\Scripts\activate

Fore macOS / Linux

-python3 -m venv venv

-source venv/bin/activate

✅ 3. Install Dependencies

Install all required Python packages:

-pip install -r requirements.txt

If you don’t have a requirements.txt, generate one:

-pip freeze > requirements.txt

✅ 4. Apply Migrations

Django needs to create the database tables.

-python manage.py migrate

✅ 5. Create a Superuser (Admin)

Optional, but useful for testing.

-python manage.py createsuperuser

Enter:
-Username
-Email
-Password

✅ 6. Run the Development Server

-python manage.py runserver

The app is now available at:
http://127.0.0.1:8000/

✅ 7. Test the App

You can now:

-Register a new user
-Log in
-View membership plans
-Purchase a plan
-View your purchases
-Test security functionality (IDOR, SQLi, Secure Cookies)

