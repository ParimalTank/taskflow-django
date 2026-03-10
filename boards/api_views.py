from rest_framework import generics
from organizations.models import Membership
from .models import Board
from .serializers import BoardSerializer


class BoardListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        org_ids = Membership.objects.filter(user=self.request.user).values_list('organization_id', flat=True)
        return Board.objects.filter(organization_id__in=org_ids)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        org_ids = Membership.objects.filter(user=self.request.user).values_list('organization_id', flat=True)
        return Board.objects.filter(organization_id__in=org_ids)
