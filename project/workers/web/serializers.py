from rest_framework import serializers


class BaseWebSerializer(serializers.Serializer):
    target = serializers.CharField()


class SqlInjectionSerializer(BaseWebSerializer):
    ...

class DirEnumerationSerializer(BaseWebSerializer):
    ...