from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        (True, 'Judge'),
        (False, 'Participant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=32)
    participant_number = models.PositiveIntegerField(default=0) # TODO: разобраться с уникальностью номеров
    role = models.BooleanField(choices=ROLE_CHOICES, default=False)
