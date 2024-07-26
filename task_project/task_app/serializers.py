from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField()
    assigned_to_username = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    last_updated_by_username = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'description', 
            'creator', 
            'assigned_to', 
            'status', 
            'created_at', 
            'updated_at', 
            'created_by_username', 
            'assigned_to_username', 
            'created_date', 
            'last_updated_by_username'
        ]

    def get_created_by_username(self, obj):
        return obj.creator.username if obj.creator else 'Unknown'

    def get_assigned_to_username(self, obj):
        return obj.assigned_to.username if obj.assigned_to else 'Unassigned'

    def get_created_date(self, obj):
        return obj.created_at.strftime('%B %d, %Y %H:%M:%S') if obj.created_at else 'No Date'

    def get_last_updated_by_username(self, obj):
        return obj.last_updated_by.username if obj.last_updated_by else 'Unknown'

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%B %d, %Y %H:%M:%S') if obj.updated_at else 'No Date'

class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()