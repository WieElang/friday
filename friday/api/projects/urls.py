from django.urls import path
from .views import ProjectIndex

app_name = "projects"

urlpatterns = [
    path('', ProjectIndex.as_view(), name='index'),
]
