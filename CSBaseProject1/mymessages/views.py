from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db import connection
from django.contrib.auth.decorators import login_required

from .models import Message

@login_required
def index(request):
    user = request.user
    my_messages = Message.objects.filter(receiver=user)

    all_users = get_user_model().objects.all()

    template = loader.get_template('index.html')
    context = {
        'my_messages': my_messages,
        'all_users': all_users,
        'user': user,
    }
    return HttpResponse(template.render(context, request))

@login_required
def sendView(request):
    new_message = request.POST.get('message')
    sender = request.user
    receiver = request.POST.get('to')
    action = request.POST.get('action')

    if action == 'Send':
        with connection.cursor() as cursor:
            cursor.executescript(
                '''INSERT INTO mymessages_message
                (receiver, sender, sent_date, message_text)
                VALUES ('{0}', '{1}', '{2}', '{3}')'''
                .format(receiver, sender, datetime.now(), new_message))

        return redirect('/')

    else:
        message_length = len(new_message)
        char_count = f'''
        <html>
          <body>
            <p>The character count for {new_message} is {message_length}.</p>
            <p><a href="/">Back</a></p>
          </body>
        </html>'''
        
        return HttpResponse(char_count)

def profileView(request):
    user = request.user #GET.get('user')
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