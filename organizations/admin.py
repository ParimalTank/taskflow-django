from django.contrib import admin
from .models import Organization, Membership, Invitation


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_by', 'created_at']
    search_fields = ['name']
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'joined_at']
    list_filter = ['role']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['invited_user', 'organization', 'role', 'status', 'invited_by', 'created_at']
    list_filter = ['status']
