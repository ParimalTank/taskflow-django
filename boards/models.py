from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization


class Board(models.Model):
    """
    A Board belongs to an Organization.
    All org members can view it; the creator owns it.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='boards')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
