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

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📘 6. Usage Guidelines
This segment clarifies how to operate with the SecureFit app when it is launched.

✅ 1. Home Page

Visit: http://127.0.0.1:8000/

Displays:

- Active membership plans
- Available gym branches
- Linking to navigation (Register, Login, Plans, Purchases)

✅ 2. Register a User

Navigate to: /register/

Enter:

- Username
- Email
- Password

After submission:

- Securely hashed password (PBKDF2).
- User log in automatically.

✅ 3. Login

Navigate to: /login/

Enter valid credentials

Authentication is made with the help of Django secure authentication backend.

✅ 4. View Plans

Navigate to: /plans/

Displays all membership plans that are active with prices and length.

✅ 5. Purchase a Plan

Click on a plan and purchases page opens.

Choose a gym branch

Submit purchase

Purchase gets saved with:

- User
- Branch
- Membership plan
- Status (default: pending)

✅ 6. View Your Purchases

Navigate to: /my-purchases/

Displays the purchases of the user who is logged in.

Added provides a connection with the receipt detailing page /purchase-detail/<id>

❗ Note on Functionality

Users that are not authorized automatically get redirected to the login page.

Secure session handling deters:

- Cross-site cookie use
- Session hijacking
- Illegitimate access of purchase information.
  

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🔐 6. Security Improvements

This applicationinitially had several purposely added security flaws.
The following security improvements were put in place to upgrade the platform into a safer release.

✅ 1. SQL Injection Prevention

Flaw: Authentication function ran direct SQL strings

Fix Implemented:
- Swapped out plain SQL statements using Django's built-in authentication.
- Runs sanitized query inputs within the framework.
- Blocks malicious SQL inputs like ' OR '1'='1.

➡️ Outcome:  neutralizes SQL exploitation user sign-in flow.

✅ 2. IDOR (Insecure Direct Object Reference) Fix

Flaw: /purchase-detail/<id> permitted end-users by editing the URL value in the request path

Fix Implemented:
- applied rigid authorization validation
- CODE: purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
- If the purchase isn’t owned by current user show inaccessible.
➡️ Outcome:
- mitigates unauthorized user-to-user data disclosure.

✅ 3. Secure Cookie & Session Hardening
Flaw: Cookies were exposed by JavaScript and shared between domains.

Fix Implemented:
- SESSION_COOKIE_HTTPONLY = True // Cookies not readable by JavaScript immune to script attacks
- SESSION_COOKIE_SECURE = True//Cookies transmitted only over TLS-protected channel
- SESSION_COOKIE_SAMESITE = 'Strict'//Cookies cannot be applied again in cross-site requests.
  
➡️ Outcome: Prevents unauthorized session capture, token theft, and cross-site request forgery misuse. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🧪 7. Testing Process
Security evaluation was executed on both versions the weak and secured releases of the platform  o confirm enhancements.

🔎 1. SQL Injection Testing
Tool: Browser + manual payloads
Payload Used: ' OR '1'='1
Outcomes: 
-Before fix: Skipped the login check, logged in as first database user.

-After fix : access denied, attack query handled as incorrect username/password

🔎 2. IDOR Testing
Steps: 
- User A created Purchase ID = 3
- User B logged in
- User B visited /purchase-detail/3

➡️ Outcome:
Before fix : User B could view User A’s order
After fix: Not found error returned (authorization check successful)

🔎 3. Session Hijacking Testing
Steps:
- Log in as User A (Browser 1)
- Copy session cookie
- Paste into Browser 2 manually

➡️ Outcome:
- Before fix: Browser 2 obtained complete access to the first user’s account.

- After fix: Session cookie expired, Browser 2 automatically logged out, HttpOnly & cross-site restriction prevented reuse of the session.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📚 8. Contributions & References
🧩 Frameworks & Libraries Used

Django 5.x – Backend Web Framework
https://www.djangoproject.com/

SQLite – Lightweight Database
https://www.sqlite.org/index.html

📖 Official Documentation & Technical References
🔑 Django Authentication System

Documentation on login, logout, password hashing, and authentication backends:
https://docs.djangoproject.com/en/5.2/topics/auth/

🛡️ Django CSRF Protection

How Django protects against CSRF attacks and how to configure CSRF cookies securely:
https://docs.djangoproject.com/en/5.2/ref/csrf/

🔐 Django Security Best Practices

Covers secure cookies, HTTPS, session security, clickjacking, injection prevention:
https://docs.djangoproject.com/en/5.2/topics/security/

🕵️‍♂️ Security Standards & Vulnerability References
📌 OWASP Top 10 – Web Application Security Risks

Global standard for identifying critical web vulnerabilities:
https://owasp.org/www-project-top-ten/

Relevant sections for this project:

A01:2021 – Broken Access Control (covers IDOR)
https://owasp.org/Top10/A01_2021-Broken_Access_Control/

A03:2021 – Injection (covers SQL Injection)
https://owasp.org/Top10/A03_2021-Injection/

A05:2021 – Security Misconfiguration (covers insecure cookies/settings)
https://owasp.org/Top10/A05_2021-Security_Misconfiguration/

OWASP Session Management Cheat Sheet
https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

OWASP Cross-Site Request Forgery (CSRF) Prevention Cheat Sheet
https://cheatsheetseries.owasp.org/cheatsheets/CSRF_Prevention_Cheat_Sheet.html

These references support your justification for:

Fixing SQL Injection

Fixing IDOR

Securing session cookies

Enforcing CSRF protections

-------------------------------------------------------------------------------------------------------------------------------------------------------------

🏷️ Credits

Base application and all security enhancements developed by:
Baibhav Chowdhury (Student ID: 24232033)
