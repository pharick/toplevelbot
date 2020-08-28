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
        marks = {'categories': {}}
        total = 0

        for category in range(1, 4):
            marks['categories'][category] = {}
            marks['categories'][category]['judges'] = {}
            total_category = 0

            for judge in Judge.objects.all():
                judge_name = f'{judge.first_name} {judge.last_name}'
                marks['categories'][category]['judges'][judge_name] = {}

                try:
                    rating = Rating.objects.filter(category=category - 1, participant=obj.id, judge=judge.id).get()
                    judge_marks = rating.marks
                    message = rating.message
                except ObjectDoesNotExist:
                    judge_marks = []
                    message = ''
                finally:
                    marks['categories'][category]['judges'][judge_name]['criteria'] = judge_marks
                    marks['categories'][category]['judges'][judge_name]['total_judge'] = sum(judge_marks)
                    marks['categories'][category]['judges'][judge_name]['message'] = message
                    total_category += marks['categories'][category]['judges'][judge_name]['total_judge']

            marks['categories'][category]['total_category'] = total_category
            total += marks['categories'][category]['total_category']

            marks['total'] = total

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
