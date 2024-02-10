from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from YandexAPI.views import DeviceViewSet, ScenarioViewSet

from .views import LoginView, LogoutView, UserInfoView


router = routers.DefaultRouter()
router.register(r'scenario', ScenarioViewSet, basename='scenario')
router.register(r'device', DeviceViewSet, basename='device')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('yandex/', include('YandexAPI.urls')), 
    path('telegram/', include('TelegramAPI.urls')),

    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', UserInfoView.as_view(), name='user-info'),
    
    path('v1/', include(router.urls), name='rest_framework'),
    path('v1/auth/', include('rest_framework.urls'))
    
    # path('devices/', DeviceViewSet.as_view({'get': 'list', 'post': 'create'}), name='device-list'),
    # path('devices/<int:pk>/', DeviceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='device-detail'),
    
    # path('scenario/', ScenarioViewSet.as_view({'get': 'list', 'post': 'create'}), name='scenario-list'),
    # path('scenario/<int:pk>/', ScenarioViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='scenario-detail'),
    
]