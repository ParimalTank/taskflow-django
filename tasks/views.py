import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from organizations.models import Organization, Membership
from boards.models import Board
from .models import Task
from .forms import TaskForm


def get_user_membership(user, org):
    try:
        return Membership.objects.get(user=user, organization=org)
    except Membership.DoesNotExist:
        return None


@login_required
def task_create(request, slug, board_pk):
    """Create a new task in a board."""
    org = get_object_or_404(Organization, slug=slug)
    if not get_user_membership(request.user, org):
        return redirect('org_list')

    board = get_object_or_404(Board, pk=board_pk, organization=org)
    if request.method == 'POST':
        form = TaskForm(request.POST, organization=org)
        if form.is_valid():
            task = form.save(commit=False)
            task.board = board
            if not task.assigned_to:
                task.assigned_to = request.user
            task.save()
            return redirect('board_detail', slug=org.slug, pk=board.pk)
    else:
        form = TaskForm(organization=org)
    return render(request, 'tasks/task_form.html', {'form': form, 'board': board, 'org': org, 'title': 'Add Task'})


@login_required
def task_edit(request, slug, pk):
    """Edit a task."""
    org = get_object_or_404(Organization, slug=slug)
    if not get_user_membership(request.user, org):
        return redirect('org_list')

    task = get_object_or_404(Task, pk=pk, board__organization=org)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, organization=org)
        if form.is_valid():
            form.save()
            return redirect('board_detail', slug=org.slug, pk=task.board.pk)
    else:
        form = TaskForm(instance=task, organization=org)
    return render(request, 'tasks/task_form.html', {'form': form, 'board': task.board, 'org': org, 'title': 'Edit Task'})


@login_required
def task_delete(request, slug, pk):
    """Delete a task."""
    org = get_object_or_404(Organization, slug=slug)
    if not get_user_membership(request.user, org):
        return redirect('org_list')

    task = get_object_or_404(Task, pk=pk, board__organization=org)
    board_pk = task.board.pk
    if request.method == 'POST':
        task.delete()
        return redirect('board_detail', slug=org.slug, pk=board_pk)
    return render(request, 'tasks/task_confirm_delete.html', {'task': task, 'org': org})


@login_required
@require_POST
def task_update_status(request, pk):
    """AJAX endpoint to update task status (for drag-and-drop)."""
    task = get_object_or_404(Task, pk=pk)
    org = task.board.organization
    if not get_user_membership(request.user, org):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    data = json.loads(request.body)
    new_status = data.get('status')
    valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
    if new_status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    task.status = new_status
    task.save()
    return JsonResponse({'success': True, 'status': task.status})
