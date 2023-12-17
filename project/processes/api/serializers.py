from rest_framework import serializers


class GetLastProcessInfoSerializer(serializers.Serializer):
    scenario_id = serializers.UUIDField()


class RunProcessSerializer(serializers.Serializer):
    scenario_id = serializers.UUIDField()