from django.urls import path 

from .views import user_polls

app_name = "users"

urlpatterns = [
    path("my_polls/", user_polls, name="user_polls"),
    
]
