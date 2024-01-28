from rest_framework import routers
from .views import CustomTokenObtainPairView, DeviceViewSet, LoginView
from django.urls import path, include, re_path
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('yandex/', include('YandexAPI.urls')), 
    path('telegram/', include('TelegramAPI.urls')),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='login'),
    path('v1/', include(router.urls)),
    path('v1/devices/', DeviceViewSet.as_view({'get': 'list'}), name='device-list'),

]