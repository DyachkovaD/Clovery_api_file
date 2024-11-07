# serializers.py
from rest_framework import serializers


class ImageInfoSerializer(serializers.Serializer):
    file_id = serializers.CharField(max_length=36)
    project_id = serializers.CharField(max_length=36)
    profile_id = serializers.CharField(max_length=36)
    account_id = serializers.CharField(max_length=36)
    data = serializers.DictField(child=serializers.CharField(max_length=255))