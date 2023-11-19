from typing import Dict, Any

from friday.apps.accounts.models import User
from friday.apps.issues.models import Issue, IssueCheckList, IssueActivity
from friday.apps.projects.models import Project
from friday.apps.tasks.models import Task, TaskActivity, Comment


def serialize_user(user: User) -> Dict[str, Any]:
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'employee_code': user.employee.code
    }


def serialize_project(project: Project) -> Dict[str, Any]:
    return {
        'id': project.id,
        'name': project.name,
        'priority': project.priority,
        'is_active': project.is_active,
        'created': project.created.strftime('%Y-%m-%d')
    }


def serialize_issue(issue: Issue, include_details: bool = False) -> Dict[str, Any]:
    data = {
        'id': issue.id,
        'project_id': issue.project_id,
        'creator_name': issue.creator.name,
        'title': issue.title,
        'description': issue.description,
        'link': issue.link,
        'status': issue.status,
        'priority': issue.priority,
        'deadline_date': issue.deadline_date.strftime('%Y-%m-%d'),
        'created': issue.created.strftime('%Y-%m-%d')
    }

    if include_details:
        data['checklists'] = [serialize_issue_checklist(checklist) for checklist in issue.checklists.all()]
        data['activities'] = [serialize_issue_activity(activity) for activity in issue.activities.all()]

    return data


def serialize_issue_checklist(checklist: IssueCheckList) -> Dict[str, Any]:
    return {
        'id': checklist.id,
        'issue_id': checklist.issue_id,
        'name': checklist.name,
        'description': checklist.description,
        'is_checked': checklist.is_checked
    }


def serialize_issue_activity(activity: IssueActivity) -> Dict[str, Any]:
    return {
        'id': activity.id,
        'issue_id': activity.issue_id,
        'user_name': activity.user.name,
        'message': activity.message,
        'created': activity.created.strftime('%Y-%m-%d')
    }


def serialize_task(task: Task, include_details: bool = False) -> Dict[str, Any]:
    data = {
        'id': task.id,
        'name': task.name,
        'project_id': task.project_id,
        'issue_id': task.issue_id,
        'status': task.status,
        'notes': task.notes,
        'link': task.link,
        'updated': task.updated.strftime('%Y-%m-%d'),
        'created': task.created.strftime('%Y-%m-%d')
    }

    if include_details:
        data['activities'] = [serialize_task_activity(activity) for activity in task.activities.all()]
        data['comments'] = [serialize_comment(comment) for comment in task.comments.all()]

    return data


def serialize_task_activity(activity: TaskActivity) -> Dict[str, Any]:
    return {
        'id': activity.id,
        'task_id': activity.task_id,
        'old_status': activity.old_status,
        'new_status': activity.new_status,
        'created': activity.created.strftime('%Y-%m-%d')
    }


def serialize_comment(comment: Comment) -> Dict[str, Any]:
    return {
        'id': comment.id,
        'user_name': comment.user.name,
        'task_id': comment.task_id,
        'message': comment.message,
        'created': comment.created.strftime('%Y-%m-%d')
    }
