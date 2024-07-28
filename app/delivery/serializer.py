from rest_framework import serializers


class MailDeliverySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)
    provider = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    total_recipients = serializers.IntegerField(required=True)
    comment = serializers.CharField(required=False)
