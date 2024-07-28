from rest_framework import serializers

from app.delivery.serializer import MailDeliverySerializer
from core.serializers import PaginatedSerializer


class SingleMailSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)
    sender = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    recipient = serializers.EmailField(required=True)
    subject = serializers.CharField(required=False)
    delivery = MailDeliverySerializer(many=True)


class PaginatedSingleMailSerializer(PaginatedSerializer):
    results = SingleMailSerializer(many=True)


class SendSingleMailSerializer(serializers.Serializer):
    sender = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    recipient = serializers.EmailField(required=True)
    subject = serializers.CharField(required=True)
    html_body = serializers.CharField(required=True)
    text_body = serializers.CharField(required=False)


class SendSingleMailTemplateSerializer(serializers.Serializer):
    sender = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    recipient = serializers.EmailField(required=True)
    subject = serializers.CharField(required=True)
    template_id = serializers.UUIDField(required=False)
    template_name = serializers.CharField(required=False)
    keywords = serializers.DictField(required=False)


class SingleMailResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    is_success = serializers.BooleanField(required=True)


class QuerySingleMailSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
    min_date = serializers.DateField(required=False)
    max_date = serializers.DateField(required=False)
    date_column = serializers.CharField(required=False)
    sort_order = serializers.CharField(required=False)
    sort_by = serializers.CharField(required=False)
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=50)
