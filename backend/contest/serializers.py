from rest_framework import serializers

from .models import Judge, Participant, Rating, ParticipantSession


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    criteria_marks = serializers.SerializerMethodField()
    total_categories = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'

    def get_criteria_marks(self, obj):
        criteria_marks = {}

        for category in range(1, 4):
            criteria_marks[category] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            for rating in Rating.objects.filter(category=category - 1, participant=obj.id):
                for i in range(10):
                    criteria_marks[category][i] += rating.marks[i]

        return criteria_marks

    def get_total_categories(self, obj):
        total_categories = {}
        criteria_marks = self.get_criteria_marks(obj)

        for category in range(1, 4):
            total_categories[category] = 0

            for i in range(10):
                total_categories[category] += criteria_marks[category][i]

        return total_categories

    def get_total(self, obj):
        total = 0
        total_categories = self.get_total_categories(obj)

        for category in range(1, 4):
            total += total_categories[category]

        return total


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
