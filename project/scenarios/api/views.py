import xxhash
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
import base64
import yaml

from project.scenarios.api.serializers import ListScenariosModelSerializer, UploadFileSerializer, \
    GetScenarioModelSerializer, UpdateScenarioSerializer
from project.processes.tasks import run_workers
from project.scenarios.models import Scenario, ScenarioBlock
from project.processes.models import Process
from project.utils.response import ResponseHandlerMixin
from project.workers.consts import ParentWorker
from project.workers.manager import worker_manager
from project.scenarios.consts import ResponseError
from project.utils.decorators import log_viewset_method


class ScenarioViewSet(ViewSet, ResponseHandlerMixin):
    permission_classes = (IsAuthenticated, )

    @log_viewset_method()
    def upload(self, request: Request):
        serializer = UploadFileSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(message=serializer.error_messages)

        try:
            decoded_file = base64.b64decode(
                serializer.validated_data.get("file")
            ).decode("utf-8")
            yaml_dict = yaml.load(decoded_file, yaml.FullLoader)
        except yaml.YAMLError as ex:
            return self.error_response(message=ResponseError.INVALID_SYNTAX.value)
        except Exception as ex:
            return self.error_response(message=ResponseError.UNKNOWN_FILE_STRUCTURE.value)
        try:
            if yaml_dict.get("version") != '1.0':
                return self.error_response(message=ResponseError.INVALID_LANGUAGE_VERSION.value)

            if not yaml_dict.get("services"):
                return self.error_response(message=ResponseError.SERVICES_NOT_FOUND.value)
        except:
            return self.error_response(message=ResponseError.UNKNOWN_FILE_STRUCTURE.value)

        try:
            Scenario.objects.get(
                name=serializer.validated_data.get("name"),
                owner=request.user
            )
            return self.error_response(message=ResponseError.SCENARIO_WITH_THIS_NAME_ALREADY_EXISTS.value)
        except:
            pass

        try:
            sc = Scenario.objects.create(
                name=serializer.validated_data.get("name"),
                description=serializer.validated_data.get("description"),
                value=yaml_dict,
                text=decoded_file,
                hashsum=xxhash.xxh3_128_hexdigest(decoded_file),
                owner=request.user
            )
        except:
            return self.error_response(message=ResponseError.SCENARIO_ALREADY_EXISTS.value)


        services = yaml_dict.get("services", {})

        for key, value in services.items():
            if key not in (
                ParentWorker.NETWORK.value,
                ParentWorker.SCANNER.value,
                ParentWorker.APPLICATION.value,
                ParentWorker.WEB.value
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

    @log_viewset_method()
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

    @log_viewset_method()
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

    def get(self, request: Request):
        scenario_id = request.query_params.get("id")
        try:
            sc = Scenario.objects.get(
                owner=request.user,
                id=scenario_id
            )
        except Scenario.DoesNotExists:
            return self.error_response(message=ResponseError.SCENARIO_NOT_FOUND.value)
        except Exception as ex:
            return self.error_response(message=ResponseError.UNKNOWN_ERROR.value)

        return self.success_response(
            body=GetScenarioModelSerializer(instance=sc).data
        )

    @log_viewset_method()
    def update(self,request: Request):
        serializer = UpdateScenarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sc = Scenario.objects.get(
                owner=request.user,
                id=serializer.validated_data.get("id")
            )
        except:
            return self.error_response(ResponseError.SCENARIO_NOT_FOUND.value)

        try:
            decoded_file = base64.b64decode(
                serializer.validated_data.get("file")
            ).decode("utf-8")
            yaml_dict = yaml.load(decoded_file, yaml.FullLoader)
        except yaml.YAMLError as ex:
            return self.error_response(message=ResponseError.INVALID_SYNTAX.value)
        except Exception as ex:
            return self.error_response(message=ResponseError.UNKNOWN_FILE_STRUCTURE.value)
        try:
            if yaml_dict.get("version") != '1.0':
                return self.error_response(message=ResponseError.INVALID_LANGUAGE_VERSION.value)

            if not yaml_dict.get("services"):
                return self.error_response(message=ResponseError.SERVICES_NOT_FOUND.value)
        except:
            return self.error_response(message=ResponseError.UNKNOWN_FILE_STRUCTURE.value)

        sc.text = decoded_file
        sc.value = yaml_dict
        sc.hashsum = xxhash.xxh3_128_hexdigest(decoded_file)
        sc.save()

        ScenarioBlock.objects.filter(
            scenario=sc
        ).delete()

        services = yaml_dict.get("services", {})

        for key, value in services.items():
            if key not in (
                    ParentWorker.NETWORK.value,
                    ParentWorker.SCANNER.value,
                    ParentWorker.APPLICATION.value,
                    ParentWorker.WEB.value
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

        return self.success_response(body={"id": sc.id})
