from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParcelViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'parcels', ParcelViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]