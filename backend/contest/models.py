from django.db import models


class Judge(models.Model):
    telegram_username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Participant(models.Model):
    telegram_username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos')
