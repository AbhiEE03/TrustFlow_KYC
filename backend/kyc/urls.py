from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MerchantKYCViewSet, ReviewerQueueViewSet

router = DefaultRouter()
router.register(r'merchant', MerchantKYCViewSet, basename='merchant-kyc')
router.register(r'reviewer/queue', ReviewerQueueViewSet, basename='reviewer-queue')

urlpatterns = [
    path('', include(router.urls)),
]
