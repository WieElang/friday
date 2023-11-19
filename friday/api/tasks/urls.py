from django.urls import path
from .views import TaskIndex, DailyTaskIndex, TaskDetails, AddTask, EditTask, DeleteTask

app_name = "tasks"

urlpatterns = [
    path('', TaskIndex.as_view(), name='index'),
    path('daily', DailyTaskIndex.as_view(), name='daily_task'),
    path('details', TaskDetails.as_view(), name='details'),
    path('add-task', AddTask.as_view(), name='add_task'),
    path('edit-task', EditTask.as_view(), name='edit_task'),
    path('delete', DeleteTask.as_view(), name='delete_task')
]
