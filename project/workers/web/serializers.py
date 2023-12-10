from rest_framework import serializers


class BaseWebSerializer(serializers.Serializer):
    target = serializers.CharField()


class SqlInjectionSerializer(BaseWebSerializer):
    exploit = serializers.BooleanField(required=False, allow_null=True, default=True)


class DirEnumerationSerializer(BaseWebSerializer):
    random_agent = serializers.BooleanField(required=False, allow_null=True, default=True)