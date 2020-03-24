from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import Judge, Participant, Rating, ParticipantSession


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    marks = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'

    def get_marks(self, obj):
        marks = {}

        for category in range(1, 4):
            marks[category] = {}

            for judge in Judge.objects.all():
                judge_name = f'{judge.first_name} {judge.last_name}'

                try:
                    judge_marks = Rating.objects.filter(category=category - 1, participant=obj.id, judge=judge.id).get().marks
                except ObjectDoesNotExist:
                    judge_marks = []
                finally:
                    marks[category][judge_name] = judge_marks

        return marks


class RatingSerializer(serializers.ModelSerializer):
    marks = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=5)
    )

    class Meta:
        model = Rating
        fields = '__all__'


class ParticipantSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantSession
        fields = '__all__'
