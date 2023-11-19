from typing import Any, Dict

from django import forms

from friday.apps.accounts.models import User
from friday.apps.issues.models import Issue, IssueCheckList


class IssueDetailForm(forms.Form):
    issue = forms.ModelChoiceField(queryset=None)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['issue'].queryset = user.assigned_issues.all()\
            .select_related('creator')\
            .prefetch_related('activities', 'checklists')


class EditStatusIssueForm(forms.Form):
    issue = forms.ModelChoiceField(queryset=None)
    status = forms.TypedChoiceField(choices=Issue.Status.choices, coerce=int)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['issue'].queryset = self.user.assigned_issues.all()

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        issue = cleaned_data['issue']
        status = cleaned_data['status']

        if issue.status == status:
            raise forms.ValidationError("Can't edit to same status", 'invalid_status')

        return cleaned_data

    def save(self) -> Issue:
        issue = self.cleaned_data['issue']
        old_status = issue.status
        status = self.cleaned_data['status']
        issue.status = status
        issue.save(update_fields=['status'])

        issue.activities.create(
            issue=issue,
            user=self.user,
            message=f'Change status from {Issue.Status(old_status).name} to {Issue.Status(status).name}'
        )
        return issue


class EditIssueChecklistForm(forms.Form):
    checklist = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['checklist'].queryset = IssueCheckList.objects.all()

    def save(self) -> IssueCheckList:
        checklist = self.cleaned_data['checklist']
        old_checked = checklist.is_checked
        checklist.is_checked = not old_checked
        checklist.save(update_fields=['is_checked'])
        return checklist
