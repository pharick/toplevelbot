from rest_framework import viewsets, views

from .models import Judge, Participant
from .serializers import JudgeSerializer, ParticipantSerializer


class JudgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JudgeSerializer
    queryset = Judge.objects.all()


class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
