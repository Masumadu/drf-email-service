from rest_framework import serializers

from core.serializers import PaginatedSerializer


class PlaceHolderSerializer(serializers.Serializer):
    key = serializers.RegexField(required=True, regex=r"^(\d|\w)+$")
    description = serializers.CharField(required=False)
    is_sensitive = serializers.BooleanField(required=True)


class MailTemplateSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    placeholders = serializers.ListField(child=PlaceHolderSerializer(), required=False)
    file_sys_path = serializers.CharField(required=False)
    object_storage = serializers.UUIDField(required=False)


class PaginatedMailTemplateSerializer(PaginatedSerializer):
    results = MailTemplateSerializer(many=True)


class AddMailTemplateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    file = serializers.FileField(required=True)


class UpdateMailTemplateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    file = serializers.FileField(required=False)


class QueryMailTemplateSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False)
    sort_order = serializers.CharField(required=False)
    sort_by = serializers.CharField(required=False)
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=50)
