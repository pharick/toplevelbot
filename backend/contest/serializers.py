from rest_framework import serializers

from .models import Judge, Participant, Rating, ParticipantSession


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    # average_marks = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'

    # def get_average_marks(self, obj):
    #     sums = {
    #         'beauty': 0,
    #         'color': 0,
    #         'shape': 0,
    #     }
    #
    #     count = 0
    #
    #     for rating in Rating.objects.filter(participant=obj.id):
    #         for mark in rating.marks:
    #             sums[mark] = sums.get(mark, 0) + int(rating.marks[mark])
    #         count += 1
    #
    #     average_marks = {mark: 0 if count == 0 else sums[mark] / count for mark in sums}
    #
    #     return average_marks


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
