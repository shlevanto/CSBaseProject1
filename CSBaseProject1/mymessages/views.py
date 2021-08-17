from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import get_user_model
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import connection  # unsafe
from django.contrib.auth.decorators import login_required


from .models import Message

# Create your views here.

#@login_required
def index(request):
    my_messages = Message.objects.all()
    
    # get list of all users
    all_users = get_user_model().objects.all()

    # get list of friends ie. those users that have sent me messages
    
    template = loader.get_template('index.html')
    context = {
        'my_messages': my_messages,
        'all_users': all_users
    }
    return HttpResponse(template.render(context, request))


# Vulnerability 1. Cross Site Request Forgery
# During development the send message -functionality csrf requirement was bypassed and it had not been fixed
@csrf_exempt
def sendView(request):
    new_message = request.POST.get('message')
    sender = request.POST.get('from')
    receiver = request.POST.get('to')
    action = request.POST.get('action')

    # Vulnerability 2. SQL Injection
    # this is an unsafe way of handling database queries, 
    # it makes the application vulnerable to SQL injection
    
    if action == 'Send':
        with connection.cursor() as cursor:
            cursor.executescript("INSERT INTO mymessages_message (receiver, sender, sent_date, message_text) VALUES ('{0}', '{1}', '{2}', '{3}')".format(sender, receiver, datetime.now(), new_message))

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
# you should only be able to see the e-mail of those who sent you messages
# but because we use GET request, you can use a modified url
def friendView(request):
    return HttpResponse('<html><body>Info of my friend</body></html>')