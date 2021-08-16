from django.db import models

# Create your models here.


class Message(models.Model):
    message_text = models.CharField(max_length=200)
    sent_date = models.DateTimeField('date sent')
    sender = models.CharField(null=True, max_length=50)
    receiver = models.CharField(null=True, max_length=50)

