from django.db import models
from django.contrib.postgres.fields import HStoreField


class Judge(models.Model):
    telegram_username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Participant(models.Model):
    telegram_username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos')
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Rating(models.Model):
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)
    judge_id = models.ForeignKey(Judge, on_delete=models.CASCADE)
    marks = HStoreField()
