from django.urls import path
from . import views


app_name = 'Chatbot'


urlpatterns = [
    # API endpoint for chat messages (what the JavaScript sends to)
    path('api/chat/', views.get_response, name='chatbot_response'),
    path('chat/', views.get_response, name='chat'),
    path('', views.index, name='index'),
]


