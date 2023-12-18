from rest_framework import serializers
from project.processes.models import Process


class GetLastProcessInfoSerializer(serializers.Serializer):
    scenario_id = serializers.UUIDField()


class RunProcessSerializer(serializers.Serializer):
    scenario_id = serializers.UUIDField()


class ListProcessResponseModelSerializer(serializers.ModelSerializer):
    scenario = serializers.SerializerMethodField()
    finished_at = serializers.SerializerMethodField()
    started_at = serializers.SerializerMethodField()

    def get_scenario(self, obj):
        return {
            "id": obj.scenario.id,
            "name": obj.scenario.name,
        }
    def get_finished_at(self, obj):
        return obj.finished_at.strftime("%d.%m.%Y %H:%S") if getattr(obj, "finished_at") else None

    def get_started_at(self, obj):
        return obj.started_at.strftime("%d.%m.%Y %H:%S")

    class Meta:
        model = Process
        fields = (
            "id",
            "code",
            "scenario",
            "is_completed",
            "started_at",
            "finished_at"
        )