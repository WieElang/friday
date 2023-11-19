from typing import Any, Dict, List

from django import forms
from django.utils import timezone

from friday.apps.accounts.models import User
from friday.apps.projects.models import Project
from friday.apps.tasks.models import Task


class TaskIndexForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['project'].queryset = Project.objects.all()

    def get_tasks(self) -> List[Task]:
        project = self.cleaned_data['project']
        return list(self.user.tasks.filter(project=project).order_by('-updated'))


class TaskDetailForm(forms.Form):
    task = forms.ModelChoiceField(queryset=None)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['task'].queryset = user.tasks\
            .select_related('issue')\
            .prefetch_related('activities', 'comments')


class TaskForm(forms.Form):
    task = forms.ModelChoiceField(queryset=None, required=False)
    project = forms.ModelChoiceField(queryset=None)
    issue = forms.ModelChoiceField(queryset=None)
    name = forms.CharField(max_length=255, required=False)
    status = forms.TypedChoiceField(choices=Task.Status.choices, coerce=int, required=False)
    notes = forms.CharField(required=False)
    link = forms.CharField(max_length=255, required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['task'].queryset = self.user.tasks.all()
        self.fields['project'].queryset = Project.objects.all()
        self.fields['issue'].queryset = self.user.assigned_issues.all()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data

        project = cleaned_data['project']
        issue = cleaned_data['issue']

        if issue.assigned != self.user:
            raise forms.ValidationError('Issue is not assigned to you', 'invalid_issue')

        if issue.project != project:
            raise forms.ValidationError('Issue not in project', 'invalid_issue_and_project')

        return cleaned_data

    def save(self) -> Task:
        task = self.cleaned_data['task']
        project = self.cleaned_data['project']
        issue = self.cleaned_data['issue']
        name = self.cleaned_data['name']
        status = self.cleaned_data['status']
        notes = self.cleaned_data['notes']
        link = self.cleaned_data['link']

        if task:
            old_status = task.status
            task.issue = issue
            task.name = name
            task.status = status
            task.notes = notes
            task.link = link
            task.updated = timezone.localdate()
            task.save(update_fields=['issue', 'name', 'status', 'notes', 'link', 'updated'])

            task.activities.create(
                task=task,
                old_status=old_status,
                new_status=status
            )
            return task

        new_task = Task.objects.create(
            name=name, user=self.user, project=project, issue=issue,
            status=Task.Status.TODO, notes=notes, link=link
        )
        return new_task


class EditStatusTaskForm(forms.Form):
    task = forms.ModelChoiceField(queryset=None)
    status = forms.TypedChoiceField(choices=Task.Status.choices, coerce=int)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['task'].queryset = self.user.tasks.all()

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        task = cleaned_data['task']
        status = cleaned_data['status']

        if task.status == status:
            raise forms.ValidationError("Can't edit to same status", 'invalid_status')

        return cleaned_data

    def save(self) -> Task:
        task = self.cleaned_data['task']
        old_status = task.status
        status = self.cleaned_data['status']
        task.status = status
        task.updated = timezone.localdate()
        task.save()

        task.activities.create(
            task=task,
            old_status=old_status,
            new_status=status
        )
        return task


class DeleteTaskForm(forms.Form):
    task = forms.ModelChoiceField(queryset=None)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['task'].queryset = self.user.tasks.all()

    def delete(self) -> None:
        task = self.cleaned_data['task']
        task.delete()
