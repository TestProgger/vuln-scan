from rest_framework import serializers
from project.scenarios import models


class ListScenariosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scenario,
        fields = (
            "id",
            "name",
            "type",
            "created_at",
            "updated_at"
        )


class UploadFileSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True, required=True)
    file = serializers.CharField()