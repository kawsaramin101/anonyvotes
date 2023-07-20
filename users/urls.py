from django.urls import path 

from .views import user_polls, close_poll, login, signup, logout

app_name = "users"

urlpatterns = [
    path("my_polls/", user_polls, name="user_polls"),
    path("close-poll/<str:secondary_id>/", close_poll, name="close_poll"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    
]
