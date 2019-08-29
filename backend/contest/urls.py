from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JudgeViewSet, ParticipantViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'judges', JudgeViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
