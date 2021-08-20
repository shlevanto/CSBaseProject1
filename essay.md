LINK: https://github.com/shlevanto/CSBaseProject1.git

The repository contains a Django app with database. It should work without any installation if you have installed Django as per instructed in the course materials.

The app is a simple messaging app. With the following features:
1. Login
2. User can see all messages sent to them
3. User can send messages other users
4. User can check character count of message they intend to send
5. User can see their user profile (username, first and last name, email)

The application contains the following vulnerabilities:

FLAW 1: Broken Authentification. The session never reaches timeout.

This flaw can not be pinpointed in the code.

If used on a public computer and the user doesn't log out, the session is left open and an attacker could access the users messages by just opening the browser and going to the app site.

The flaw can be fixed by installing middleware that allows the admin to set timeout in the settings.py file. One such middleware is django-session-timeout (see https://snyk.io/advisor/python/django-session-timeout).

FLAW 2: Security Misconfiguration

https://github.com/shlevanto/CSBaseProject1/blob/main/CSBaseProject1/admin_info

The app comes with a database and the admin access for the app is set to username: admin, password: admin. To make things worse, a file containing this information is left in the repository. This flaw is akin to having environment variables in the remoter repository.

No sensitive information should be pushed to the repository. If .env files are used, they should always be added to the .gitignore file.

FLAW 3: SQL Injection
<link>

The app uses a raw SQL-connection to communicate with the database and the query is not parametrized. This leaves the database open for SQL injections. As this is a Django app, the attacker can be expected to know that by default the user information is stored in a table called auth_user.

A quick fix would be to use cursor.execute instead of cursor.executescript as execute allows for only one database query to be executed. A more fool-proof solution is to use the Django models functionality to communicat with the database. The app has a model called Message and the correct way to create a new message would be:

Message.objects.create(
    receiver=receiver,
    sender=sender,
    message_text=new_message,
    sent_date=datetime.now()
    )

FLAW 4: XSS
<link>

The character count action takes the user input (the message) and returns an http response using the input as it is. As this creates a new html page, it is vulnerable to the insertion of malicious scripts.

This could be fixed by having the character count use an html template and rendering it. Any malicious code would be interpreted as a string and would not cause harm.

Another possibility would be to use javascript on the index.html template file to display the character count of the message.

FLAW 5: Broken Access Control
<link>

Showing the user profile has several security issues that make it possible for anyone to access the information of any user without logging into the site. This is possible because it uses a GET request that allows parameters to be set in the request URL. The app does not check if the requested profile user is logged in and actually the view even doesn't require a user to be logged in.

Requirement for having a user logged in can be fixed by adding @login_required decorator to profileView. The other views indexView and sendView have this decorator but maybe the coder forgot to decorate the newest view.

The quickest fix would be to not rely on getting the information about the user fromt the HTML template but instead write line 58 as:

user = request.user

Now the url parameter does not affect the end result.

Add source link to each flaw if appropriate. Ideally, the link should have the format https://urldomain/repo/file.py#L42 (Line 42 in file.py
