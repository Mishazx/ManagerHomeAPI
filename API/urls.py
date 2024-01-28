from rest_framework import routers
from .views import CustomTokenObtainPairView, DeviceViewSet
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')


urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/', LoginView.as_view(), name='login'),
    path('v1/', include(router.urls)),
    path('v1/devices/', DeviceViewSet.as_view({'get': 'list'}), name='device-list'),
    # path('v1/devices/<str:device_name>/', DeviceViewSet.as_view({'get': 'custom_action'}), name='device-detail'),
    # re_path(r'^v1/devices/(?P<device_name>[\w\s%]+)/$', DeviceViewSet.as_view({'get': 'custom_action'}), name='device-custom-action'),
    re_path(r'^v1/devices/(?P<device_name>[\w\s%]+)/$', DeviceViewSet.as_view({'get': 'custom_action'}), name='device-custom-action'),

]