from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import get_user_model
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth.decorators import login_required

from .models import Message

# Create your views here.

@login_required
def index(request):
    user = request.user
    my_messages = Message.objects.filter(receiver=user)

    # get list of all users
    all_users = get_user_model().objects.all()

    template = loader.get_template('index.html')
    context = {
        'my_messages': my_messages,
        'all_users': all_users,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


# Vulnerability 1. Cross Site Request Forgery
# During development the send message -functionality csrf requirement was bypassed and it had not been fixed
@csrf_exempt
def sendView(request):
    new_message = request.POST.get('message')
    sender = request.user
    receiver = request.POST.get('to')
    action = request.POST.get('action')

    # Vulnerability 2. SQL Injection
    # this is an unsafe way of handling database queries, 
    # it makes the application vulnerable to SQL injection

    if action == 'Send':
        with connection.cursor() as cursor:
            cursor.executescript(
                '''INSERT INTO mymessages_message
                (receiver, sender, sent_date, message_text)
                VALUES ('{0}', '{1}', '{2}', '{3}')'''
                .format(receiver, sender, datetime.now(), new_message))

        # using Django models to handle the database would be safe
        # also using cursor.execute only allows to execute on SQL command

        '''
        Message.objects.create(
            receiver=receiver,
            sender=sender,
            message_text=new_message,
            sent_date=datetime.now()
            )
        '''
        return redirect('/')

    else:
        # Vulnerability 3. XSS
        # The character count is passed as a string
        message_length = len(new_message)
        char_count = f'<html><body>The character count for {new_message} is {message_length}.</body></html>'
        return HttpResponse(char_count)

# Vulnerability 4. Exposure of data
# you should only be able to see your own user profile
# but because we use GET request, you can set url parameters freely
# the fix is to use request.user as a parameter for post


def profileView(request):
    user = request.GET.get('user')
    template = loader.get_template('profile.html')

    def dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM auth_user WHERE username='{0}'".format(user))
        profile = dictfetchall(cursor)[0]

    context = {
        'username': profile['username'],
        'first_name': profile['first_name'],
        'last_name': profile['last_name'],
        'email': profile['email'],
    }

    return HttpResponse(template.render(context, request))