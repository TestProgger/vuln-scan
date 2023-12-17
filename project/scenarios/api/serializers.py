from rest_framework import serializers
from project.scenarios import models


class ListScenariosModelSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%S")

    class Meta:
        model = models.Scenario
        fields = (
            "id",
            "name",
            "created_at"
        )


class GetScenarioModelSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%S")

    class Meta:
        model = models.Scenario
        fields = (
            "id",
            "name",
            "text",
            "created_at"
        )


class UpdateScenarioSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file = serializers.CharField()


class UploadFileSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    file = serializers.CharField()