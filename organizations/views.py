from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify
from .models import Organization, Membership, Invitation
from .forms import OrganizationForm, InviteForm


def get_user_org_role(user, organization):
    """Get the user's membership role in an org, or None."""
    try:
        return Membership.objects.get(user=user, organization=organization)
    except Membership.DoesNotExist:
        return None


@login_required
def org_list(request):
    """List all organizations the user belongs to."""
    memberships = Membership.objects.filter(user=request.user).select_related('organization')
    pending_invites = Invitation.objects.filter(invited_user=request.user, status='PENDING').select_related('organization', 'invited_by')
    return render(request, 'organizations/org_list.html', {
        'memberships': memberships,
        'pending_invites': pending_invites,
    })


@login_required
def org_create(request):
    """Create a new organization."""
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.created_by = request.user
            # Generate unique slug
            base_slug = slugify(org.name)
            slug = base_slug
            counter = 1
            while Organization.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            org.slug = slug
            org.save()
            # Creator becomes Owner
            Membership.objects.create(user=request.user, organization=org, role='OWNER')
            messages.success(request, f'Organization "{org.name}" created!')
            return redirect('org_detail', slug=org.slug)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/org_form.html', {'form': form, 'title': 'Create Organization'})


@login_required
def org_detail(request, slug):
    """Organization dashboard — shows boards and members."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_org_role(request.user, org)
    if not membership:
        messages.error(request, "You don't have access to this organization.")
        return redirect('org_list')

    boards = org.boards.all()
    members = Membership.objects.filter(organization=org).select_related('user')
    pending_invites = Invitation.objects.filter(organization=org, status='PENDING').select_related('invited_user')

    return render(request, 'organizations/org_detail.html', {
        'org': org,
        'membership': membership,
        'boards': boards,
        'members': members,
        'pending_invites': pending_invites,
    })


@login_required
def org_edit(request, slug):
    """Edit an organization (Owner/Admin only)."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_org_role(request.user, org)
    if not membership or membership.role not in ('OWNER', 'ADMIN'):
        messages.error(request, "You don't have permission to edit this organization.")
        return redirect('org_detail', slug=org.slug)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization updated!')
            return redirect('org_detail', slug=org.slug)
    else:
        form = OrganizationForm(instance=org)
    return render(request, 'organizations/org_form.html', {'form': form, 'title': 'Edit Organization', 'org': org})


@login_required
def org_invite(request, slug):
    """Invite a user to the organization (Owner/Admin only)."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_org_role(request.user, org)
    if not membership or membership.role not in ('OWNER', 'ADMIN'):
        messages.error(request, "You don't have permission to invite members.")
        return redirect('org_detail', slug=org.slug)

    if request.method == 'POST':
        form = InviteForm(request.POST, organization=org)
        if form.is_valid():
            invited_user = User.objects.get(username=form.cleaned_data['username'])
            Invitation.objects.create(
                organization=org,
                invited_by=request.user,
                invited_user=invited_user,
                role=form.cleaned_data['role'],
            )
            messages.success(request, f'Invitation sent to "{invited_user.username}"!')
            return redirect('org_detail', slug=org.slug)
    else:
        form = InviteForm(organization=org)
    return render(request, 'organizations/org_invite.html', {'form': form, 'org': org})


@login_required
def invite_accept(request, pk):
    """Accept an invitation."""
    invite = get_object_or_404(Invitation, pk=pk, invited_user=request.user, status='PENDING')
    if request.method == 'POST':
        Membership.objects.create(
            user=request.user,
            organization=invite.organization,
            role=invite.role,
        )
        invite.status = 'ACCEPTED'
        invite.save()
        messages.success(request, f'You joined "{invite.organization.name}"!')
        return redirect('org_detail', slug=invite.organization.slug)
    return redirect('org_list')


@login_required
def invite_decline(request, pk):
    """Decline an invitation."""
    invite = get_object_or_404(Invitation, pk=pk, invited_user=request.user, status='PENDING')
    if request.method == 'POST':
        invite.status = 'DECLINED'
        invite.save()
        messages.info(request, f'Invitation to "{invite.organization.name}" declined.')
    return redirect('org_list')


@login_required
def org_remove_member(request, slug, user_id):
    """Remove a member from the organization (Owner only)."""
    org = get_object_or_404(Organization, slug=slug)
    membership = get_user_org_role(request.user, org)
    if not membership or membership.role != 'OWNER':
        messages.error(request, "Only the owner can remove members.")
        return redirect('org_detail', slug=org.slug)

    target_membership = get_object_or_404(Membership, user_id=user_id, organization=org)
    if target_membership.role == 'OWNER':
        messages.error(request, "Cannot remove the owner.")
        return redirect('org_detail', slug=org.slug)

    if request.method == 'POST':
        target_membership.delete()
        messages.success(request, f'Member removed from organization.')
    return redirect('org_detail', slug=org.slug)
