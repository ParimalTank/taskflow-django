from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'board', 'assigned_to', 'created_at', 'updated_at']
