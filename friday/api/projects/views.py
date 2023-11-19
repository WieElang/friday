from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from friday.api.views import SessionAPIView
from friday.apps.projects.models import Project
from friday.core.serializer import serialize_project


class ProjectIndex(SessionAPIView):
    def get(self, request: Request) -> Response:

        data = {'projects': []}
        employee = request.user.employee

        if not employee:
            return Response(data=data, status=status.HTTP_200_OK)

        project_ids = employee.teams.values_list('projects', flat=True)
        projects = Project.objects.filter(id__in=project_ids).order_by('-priority')

        data['projects'] = [serialize_project(project) for project in projects]
        return Response(data=data, status=status.HTTP_200_OK)
