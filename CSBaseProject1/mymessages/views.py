from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import get_user_model
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import connection  # unsafe


from .models import Message

# Create your views here.


def index(request):
    my_messages = Message.objects.all()
    
    # get list of all users
    # this also shows tha admin username!
    all_users = get_user_model().objects.all()

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
    
    # Vulnerability 2. SQL Injection
    # this is an unsafe way of handling database queries, 
    # it makes the application vulnerable to SQL injection
    
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