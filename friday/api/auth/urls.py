from django.urls import path
from .views import Login, Logout, Profile

app_name = "auth"

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('profile', Profile.as_view(), name='profile'),
    path('logout', Logout.as_view(), name='logout'),
]
