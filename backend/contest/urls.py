from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JudgeViewSet, ParticipantViewSet, RatingViewSet, ParticipantSessionViewSet

router = DefaultRouter()
router.register(r'judges', JudgeViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'participant-sessions', ParticipantSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
