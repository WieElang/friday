from django.conf.urls import include
from django.urls import path

app_name = "api"

urlpatterns = [
    path('auth/', include('friday.api.auth.urls', namespace='auth')),
    path('issues/', include('friday.api.issues.urls', namespace='issues')),
    path('projects/', include('friday.api.projects.urls', namespace='projects')),
    path('tasks/', include('friday.api.tasks.urls', namespace='tasks')),
]
