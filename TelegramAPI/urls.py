from django.urls import path
from .views import UpdateBot
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('webhook/', csrf_exempt(UpdateBot.as_view()), name='update'), 
]
