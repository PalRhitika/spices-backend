from rest_framework import serializers
from .models import Connection
from users.models import User

class ConnectionReadSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(source='from_user.full_name', read_only=True)
    to_user = serializers.CharField(source='to_user.full_name', read_only=True)
    class Meta:
        model = Connection
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['from_user', 'status', 'created_at']

class ConnectionSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(source='from_user.full_name', read_only=True)
    to_user = serializers.CharField(source='to_user.full_name', read_only=False)
    class Meta:
        model = Connection
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['from_user', 'status', 'created_at']

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'contact_number', 'company_name', 'industry', 'username']
