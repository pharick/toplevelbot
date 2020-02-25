from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


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
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)

    CATEGORY_CHOICES = [
        (0, 'Акварельные губы'),
        (1, 'Веки с растушевкой'),
        (2, 'Пудровые брови')
    ]
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)

    marks = ArrayField(models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)]))


class ParticipantSession(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    chat_id = models.PositiveIntegerField(unique=True)
