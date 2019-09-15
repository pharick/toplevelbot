from django.contrib import admin

from .models import Judge, Participant, Rating

admin.site.register(Judge)
admin.site.register(Participant)
admin.site.register(Rating)
