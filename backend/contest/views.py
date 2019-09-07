from rest_framework import viewsets

from .models import Judge, Participant, Rating, ParticipantSession
from .serializers import JudgeSerializer, ParticipantSerializer, RatingSerializer, ParticipantSessionSerializer


class JudgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JudgeSerializer
    queryset = Judge.objects.all()
    lookup_field = 'telegram_username'


class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    lookup_field = 'telegram_username'
    filterset_fields = ['number']


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filterset_fields = ['judge']


class ParticipantSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipantSessionSerializer
    queryset = ParticipantSession.objects.all()
    lookup_field = 'participant'
