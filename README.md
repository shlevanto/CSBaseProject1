# CSBaseProject1

This is a course project for University of Helsinki Cyber Security Base course. The purpose of this project is to use Django to build a website with at least five known vulnerabilities from the [OWASP top ten list](https://owasp.org/www-project-top-ten/) and provide information on how to fix them.

The vulnerabilities and fixes are described in the [essay.md](/essay.md) file.

## Description of the app

The website is a simple app where one can create a user profile and send messages to other users. 

The files include a database db.sqlite3 with four users if you want to try out the functionality.

## Installation
You need to have Python and Django installed to run this application
``` pip install django```

Clone the repository to your machine and locate the manage.py file. Start the appliction using

``` python manage.py runserver ```

Open your browser and go to [localhost:8000](localhost:8000).

You can log in using any one of these user accounts:

bob:squarepants

alice:redqueen

patrick:starf1sh


