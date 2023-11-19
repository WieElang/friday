from datetime import datetime, time
from django.utils import timezone

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from friday.api.responses import ErrorResponse
from friday.api.views import SessionAPIView
from friday.apps.tasks.models import Task, TaskActivity
from friday.core.serializer import serialize_issue, serialize_task, serialize_task_activity

from .forms import TaskIndexForm, TaskDetailForm, TaskForm, EditStatusTaskForm, DeleteTaskForm


class TaskIndex(SessionAPIView):
    def get(self, request: Request) -> Response:
        form = TaskIndexForm(user=request.user, data=request.query_params)

        if form.is_valid():
            tasks = form.get_tasks()

            response = {
                'tasks': [serialize_task(task) for task in tasks]
            }
            return Response(response, status=status.HTTP_200_OK)

        return ErrorResponse(form)


class DailyTaskIndex(SessionAPIView):
    def get(self, request: Request) -> Response:
        today = timezone.localdate()
        min_today_datetime = datetime.combine(today, time.min)
        max_today_datetime = datetime.combine(today, time.max)
        task_activities = TaskActivity.objects.filter(created__gte=min_today_datetime, created__lte=max_today_datetime, task__user=request.user)\
            .order_by('-created')
        task_ids = task_activities.values_list('task_id', flat=True)
        tasks = Task.objects.filter(id__in=task_ids)

        response = {
            'tasks': [serialize_task(task) for task in tasks],
            'activities': [serialize_task_activity(activity) for activity in task_activities]
        }

        return Response(response, status=status.HTTP_200_OK)


class TaskDetails(SessionAPIView):
    def get(self, request: Request) -> Response:
        form = TaskDetailForm(user=request.user, data=request.query_params)

        if form.is_valid():
            task = form.cleaned_data['task']

            response = {
                'task': serialize_task(task, include_details=True),
                'issue': serialize_issue(task.issue)
            }
            return Response(response, status=status.HTTP_200_OK)

        return ErrorResponse(form)


class AddTask(SessionAPIView):
    def post(self, request: Request) -> Response:
        form = TaskForm(user=request.user, data=request.data)
        if form.is_valid():
            task = form.save()

            data = {
                'status': 'ok',
                'task': serialize_task(task)
            }
            return Response(data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class EditTask(SessionAPIView):
    def post(self, request: Request) -> Response:
        form = TaskForm(user=request.user, data=request.data)
        if form.is_valid():
            task = form.save()

            data = {
                'status': 'ok',
                'task': serialize_task(task)
            }
            return Response(data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class EditStatusTask(SessionAPIView):
    def post(self, request: Request) -> Response:
        form = EditStatusTaskForm(user=request.user, data=request.data)
        if form.is_valid():
            task = form.save()

            data = {
                'status': 'ok',
                'task': serialize_task(task)
            }
            return Response(data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class DeleteTask(SessionAPIView):
    def post(self, request: Request) -> Response:
        form = DeleteTaskForm(user=request.user, data=request.data)
        if form.is_valid():
            form.delete()

            data = {
                'status': 'ok'
            }
            return Response(data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
