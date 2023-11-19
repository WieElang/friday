from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from friday.api.responses import ErrorResponse
from friday.api.views import SessionAPIView
from friday.apps.issues.models import Issue
from friday.core.serializer import serialize_issue

from .forms import IssueDetailForm, EditStatusIssueForm, EditIssueChecklistForm


class IssueIndex(SessionAPIView):
    def get(self, request: Request) -> Response:
        issues = Issue.objects.filter(assigned=request.user)\
            .select_related('creator')\
            .order_by('-priority')
        response = {'issues': [serialize_issue(issue) for issue in issues]}
        return Response(response, status=status.HTTP_200_OK)


class IssueDetail(SessionAPIView):
    def get(self, request: Request) -> Response:
        form = IssueDetailForm(user=request.user, data=request.query_params)
        if form.is_valid():
            issue = form.cleaned_data['issue']

            response = {
                'issue': serialize_issue(issue, include_details=True)
            }
            return Response(response, status=status.HTTP_200_OK)

        return ErrorResponse(form)


class EditStatusIssue(SessionAPIView):
    def post(self, request: Request) -> Response:
        form = EditStatusIssueForm(user=request.user, data=request.data)
        if form.is_valid():
            issue = form.save()

            data = {
                'status': 'ok',
                'issue': serialize_issue(issue)
            }
            return Response(data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class EditChecklist(SessionAPIView):
    def post(self, request: Request) -> Response:
        form = EditIssueChecklistForm(data=request.data)
        if form.is_valid():
            form.save()

            data = {
                'status': 'ok'
            }
            return Response(data, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
