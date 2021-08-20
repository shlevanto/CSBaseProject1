LINK: https://github.com/shlevanto/CSBaseProject1.git

The repository contains a Django app with database. It should work without any installation if you have installed Django as per instructed in the course materials.

The app is a simple messaging app. With the following features:
1. Login
2. User can see all messages sent to them
3. User can send messages other users
4. User can check character count of message they intend to send
5. User can see their user profile (username, first and last name, email)

The application contains the following vulnerabilties:

FLAW 1: Broken Authentification. The session never reaches timeout.

This flaw can not be pinponted in the code.

If used on a public computer and the user doesn't log out, the session is left open and an attacker could access the users messages by just opening the browser and going to the app site.

The flaw can be fixed by installing middleware that allows the admin to set timeout in the settings.py file. One such middleware is django-session-timeout (see https://snyk.io/advisor/python/django-session-timeout).

FLAW 2: Security Misconfiguration

https://github.com/shlevanto/CSBaseProject1/blob/main/CSBaseProject1/admin_info

The app comes with a database and the admin access for the app is set to username: admin, password: admin. To make things worse, a file containing this information is left in the repository. This flaw is akin to having environment variables in the remoter repository. 

No sensitive information should be pushed to the repository. If .env files are used, they should always be added to the .gitignore file.

FLAW 3: SQL Injection

FLAW 4: XSS

FLAW 5: Broken Access ControlAdd source link to each flaw if appropriate. Ideally, the link should have the format https://urldomain/repo/file.py#L42 (Line 42 in file.py
