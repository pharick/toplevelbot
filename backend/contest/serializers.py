from rest_framework import serializers

from .models import Judge, Participant, Rating


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    marks = serializers.DictField()

    class Meta:
        model = Rating
        fields = '__all__'
