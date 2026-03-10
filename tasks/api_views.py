from rest_framework import generics
from organizations.models import Membership
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        org_ids = Membership.objects.filter(user=self.request.user).values_list('organization_id', flat=True)
        return Task.objects.filter(board__organization_id__in=org_ids)

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        org_ids = Membership.objects.filter(user=self.request.user).values_list('organization_id', flat=True)
        return Task.objects.filter(board__organization_id__in=org_ids)
