from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from organizations.models import Organization, Membership
from .models import Board
from .forms import BoardForm


def get_user_membership(user, org):
    try:
        return Membership.objects.get(user=user, organization=org)
    except Membership.DoesNotExist:
        return None


@login_required
def board_list(request, slug):
    """Show all boards in an organization."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_membership(request.user, org)
    if not membership:
        return redirect('org_list')
    boards = org.boards.all()
    return render(request, 'boards/board_list.html', {'boards': boards, 'org': org, 'membership': membership})


@login_required
def board_create(request, slug):
    """Create a new board in an organization."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_membership(request.user, org)
    if not membership:
        return redirect('org_list')

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.organization = org
            board.owner = request.user
            board.save()
            return redirect('board_detail', slug=org.slug, pk=board.pk)
    else:
        form = BoardForm()
    return render(request, 'boards/board_form.html', {'form': form, 'title': 'Create Board', 'org': org})


@login_required
def board_detail(request, slug, pk):
    """Show a single board with Kanban view."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_membership(request.user, org)
    if not membership:
        return redirect('org_list')

    board = get_object_or_404(Board, pk=pk, organization=org)
    members = Membership.objects.filter(organization=org).select_related('user')
    todo_tasks = board.tasks.filter(status='TODO')
    in_progress_tasks = board.tasks.filter(status='IN_PROGRESS')
    done_tasks = board.tasks.filter(status='DONE')
    return render(request, 'boards/board_detail.html', {
        'board': board,
        'org': org,
        'membership': membership,
        'members': members,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
    })


@login_required
def board_edit(request, slug, pk):
    """Edit a board."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_membership(request.user, org)
    if not membership:
        return redirect('org_list')

    board = get_object_or_404(Board, pk=pk, organization=org)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board_detail', slug=org.slug, pk=board.pk)
    else:
        form = BoardForm(instance=board)
    return render(request, 'boards/board_form.html', {'form': form, 'title': 'Edit Board', 'org': org})


@login_required
def board_delete(request, slug, pk):
    """Delete a board (Owner/Admin or board creator only)."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_membership(request.user, org)
    if not membership:
        return redirect('org_list')

    board = get_object_or_404(Board, pk=pk, organization=org)
    if request.method == 'POST':
        board.delete()
        return redirect('board_list', slug=org.slug)
    return render(request, 'boards/board_confirm_delete.html', {'board': board, 'org': org})
