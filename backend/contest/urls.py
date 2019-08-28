from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JudgeViewSet, ParticipantViewSet, RateViewSet

router = DefaultRouter()
router.register(r'judges', JudgeViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'rates', RateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
