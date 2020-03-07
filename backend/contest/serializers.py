from rest_framework import serializers

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

        total = 0

        for category in range(3):
            marks[category] = {
                'criteria': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'total': 0
            }

            total_category = 0

            for rating in Rating.objects.filter(category=category, participant=obj.id):
                for i in range(10):
                    marks[category]['criteria'][i] += rating.marks[i]
                    total_category += rating.marks[i]

            marks[category]['total'] = total_category
            total += total_category

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
