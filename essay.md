LINK: https://github.com/shlevanto/CSBaseProject1.git

The repository contains a Django app with database. It should work without any installation if you have installed Django as per instructed in the course materials.

The app is a simple messaging app. With the following features:
1. Login
2. User can see all messages sent to them
3. User can send messages other users
4. User can check character count of message they intend to send
5. User can see their user profile (username, first and last name, email)

The application contains the following vulnerabilities:

FLAW 1: Broken Authentication.

This flaw can not be pinpointed in the code as it is something that is completely missing.

The session is left open indefinitely unless the user logs out. If the user doesn't log out, but only closes the browser, an attacker could access the users messages by just opening the browser and going to the app site. Actually the attacker could also send messages as the user and cause all kinds of trouble.

The flaw can be fixed by installing middleware that allows the admin to set timeout in the settings.py file. One such middleware is django-session-timeout (see https://snyk.io/advisor/python/django-session-timeout). One would however have to be careful not to choose a middleware with known vulnerabilities.

FLAW 2: Security Misconfiguration

https://github.com/shlevanto/CSBaseProject1/blob/main/CSBaseProject1/admin_info

The app comes with a database and the admin access for the app is set to username: admin, password: admin. This is a very well known vulnerability and something that a potential attacker probably would try to exploit right away. Luckily the user table in the database uses Django's authentication protocols so the passwords are encrypted. The programmer of this app however made a serious blunder. A file containing the admin password is left in the repository. This flaw is akin to having environment variables for a published app in the remote repository.

No sensitive information like this should ever be pushed to a remote repository. Instead all such files should always be added to the .gitignore file. An even better fix would be to not write the admin password in any file except a dedicated and encrypted password manager.

FLAW 3: SQL Injection
https://github.com/shlevanto/CSBaseProject1/blob/main/CSBaseProject1/mymessages/views.py#L34

The app uses a raw SQL-connection to communicate with the database and the query is not parametrized. It uses the user input from the html form as part of the SQL command. This leaves the database open for SQL injections. The app is recognizable as a Django project when visiting the <url>/admin page so a potential attacker would know the default scheme of the app's database. By default the user information is stored in a table called auth_user, so an attacker could exploit the injection to wreak havoc on the app's user information.

A quick fix would be to use cursor.execute instead of cursor.executescript as execute allows for only one database query to be executed. This would however result in an error message page stating that only one query can be executed. This would signal the attacker that the query interaction with the database is flawed.

A more fool-proof solution would be to use the Django models protocol to communicate with the database. The app has a model called Message and the correct way to create a new message would be:

Message.objects.create(
    receiver=receiver,
    sender=sender,
    message_text=new_message,
    sent_date=datetime.now()
    )

FLAW 4: Cross-Site Scripting XSS
https://github.com/shlevanto/CSBaseProject1/blob/main/CSBaseProject1/mymessages/views.py#L45

The character count action on the index.html page takes the user input (the message) and returns an http response using the input as it is. As this creates a new html page without sanitizing the input in any way, it causes the app to be vulnerable to the insertion of malicious scripts.

This could be fixed by having the character count use an html template and rendering it. Any malicious code would be interpreted as a string and would not cause harm. One would need to make a charcount.html template and pass the content relating the messages character count in a context -variable similiar to the index view.

Another possibility would be to use javascript directly on the index.html template file to display the character count of the message without including the message.

FLAW 5: Broken Access Control
https://github.com/shlevanto/CSBaseProject1/blob/main/CSBaseProject1/mymessages/views.py#L34

Showing the user profile information has several security issues that make it possible for anyone to access the information of any user without logging into the site. This is possible because it uses a GET request that allows parameters to be set in the request URL. The app does not check if the requested profile user is logged in and actually the view even doesn't require a user to be logged in at all.

Requirement for having a user logged in can be fixed by adding @login_required decorator to profileView. The other views index and sendView have this decorator in place so this security flaw may have been caused by adding the profileView as a last minute feature and forgetting the decorator.

The quickest fix would be to not rely on getting the information about the user fromt the HTML template but instead write line 58 as:

user = request.user

Now the url parameter user does not affect the rendering of the profile page.
