from rest_framework import viewsets

from .models import Judge, Participant, Rate
from .serializers import JudgeSerializer, ParticipantSerializer, RateSerializer


class JudgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JudgeSerializer
    queryset = Judge.objects.all()


class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()


class RateViewSet(viewsets.ModelViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
