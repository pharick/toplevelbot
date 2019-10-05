from rest_framework import serializers

from .models import Judge, Participant, Rating, ParticipantSession


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    average_marks = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'

    def get_average_marks(self, obj):
        sums, counts = dict(), dict()

        for rating in Rating.objects.filter(participant=obj.id):
            for mark in rating.marks:
                sums[mark] = sums.get(mark, 0) + int(rating.marks[mark])
                counts[mark] = counts.get(mark, 0) + 1

        average_marks = dict()

        for mark in sums:
            average_marks[mark] = sums[mark] / counts[mark]

        return average_marks


class RatingSerializer(serializers.ModelSerializer):
    marks = serializers.DictField()

    class Meta:
        model = Rating
        fields = '__all__'


class ParticipantSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantSession
        fields = '__all__'
