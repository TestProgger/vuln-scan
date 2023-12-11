from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
import base64
import yaml

from project.scenarios.api.serializers import ListScenariosModelSerializer, UploadFileSerializer
from project.processes.tasks import run_workers
from project.scenarios.models import Scenario, ScenarioBlock
from project.processes.models import Process
from project.utils.response import ResponseHandlerMixin
from project.workers.consts import ParentWorker
from project.workers.manager import worker_manager
from project.scenarios.consts import ResponseError


class ScenarioViewSet(ViewSet, ResponseHandlerMixin):
    permission_classes = (IsAuthenticated, )

    def upload(self, request: Request):
        serializer = UploadFileSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(message=serializer.error_messages)

        try:
            decoded_file = base64.b64decode(
                serializer.validated_data.get("file")
            ).decode("utf-8")
            yaml_dict = yaml.load(decoded_file, yaml.FullLoader)
        except yaml.YAMLError:
            return self.error_response(message=ResponseError.INVALID_SYNTAX.value)
        except Exception as ex:
            return self.error_response(message=ResponseError.UNKNOWN_FILE_STRUCTURE.value)

        if yaml_dict.get("version") != '1.0':
            return self.error_response(message=ResponseError.INVALID_LANGUAGE_VERSION.value)

        if not yaml_dict.get("services"):
            return self.error_response(message=ResponseError.SERVICES_NOT_FOUND.value)


        sc = Scenario.objects.create(
            name=serializer.validated_data.get("name"),
            description=serializer.validated_data.get("description"),
            value=yaml_dict,
            owner=request.user
        )

        services = yaml_dict.get("services", {})

        for key, value in services.items():
            if key not in (
                ParentWorker.WEB.value,
                ParentWorker.NETWORK.value,
                ParentWorker.SCANNER.value,
                ParentWorker.OS.value
            ):
                return self.error_response(message=f"Неизвестная инструкция {key}")

            parent_scenario = ScenarioBlock.objects.create(
                scenario=sc,
                value=value,
                parent_instruction=key
            )

            for child_key, child_value in value.items():
                if worker_manager.check_exists(key, child_key):
                    ScenarioBlock.objects.create(
                        scenario=sc,
                        parent=parent_scenario,
                        value=child_value,
                        instruction=child_key,
                        parent_instruction=key
                    )
        return self.success_response(
            body={
                "id": sc.pk,
                "name": sc.name,
                "created_at": sc.created_at
            }
        )

    def run_scenario(self, request: Request):
        scenario_id = request.data.get("scenario_id")
        process = Process.objects.create(
            scenario_id=scenario_id,
            owner=request.user
        )

        run_workers.apply_async(
            kwargs={"process_id": process.id, "scenario_id": scenario_id}
        )

        return self.success_response(body={"scenario_id": scenario_id, "process_id": process.pk})

    def list(self, request: Request):
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        scenarios = Scenario.objects.filter(
            owner=request.user
        )

        total_count = scenarios.count()

        try:
            serializer = ListScenariosModelSerializer(
                instance=scenarios[(page-1)*page_size: page*page_size],
                many=True
            )
        except Exception as ex:
            return self.success_response(
                body={
                    "list": [],
                    "total": 0
                }
            )

        return self.success_response(
            body={
                "list": serializer.data,
                "total": total_count
            }
        )
