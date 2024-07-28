from rest_framework import serializers

from core.serializers import PaginatedSerializer


class MailAccountSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)
    mail_address = serializers.EmailField(required=True)
    sender_name = serializers.CharField(required=False)
    is_default = serializers.BooleanField(required=True)


class PaginatedMailAccountSerializer(PaginatedSerializer):
    results = MailAccountSerializer(many=True)


class AddMailAccountSerializer(serializers.Serializer):
    mail_address = serializers.EmailField(required=True)
    sender_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    is_default = serializers.BooleanField(required=False, default=False)


class UpdateMailAccountSerializer(serializers.Serializer):
    sender_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    is_default = serializers.BooleanField(required=False)


class QueryMailAccountSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False)
    sort_order = serializers.CharField(required=False)
    sort_by = serializers.CharField(required=False)
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=50)
