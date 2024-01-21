from rest_framework import routers
from .views import CustomTokenObtainPairView, DeviceViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)


urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls)),
]