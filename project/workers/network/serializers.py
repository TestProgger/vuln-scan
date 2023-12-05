from rest_framework import serializers


class ArpPoisonSerializer(serializers.Serializer):
    target = serializers.CharField()
    interface = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    gateway = serializers.CharField(required=False, allow_blank=True, allow_null=True)

