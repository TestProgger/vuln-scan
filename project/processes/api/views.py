import json

import transliterate
from django.utils.text import slugify
from django.db.models import QuerySet
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from project.utils.decorators import log_viewset_method
from project.utils.response import ResponseHandlerMixin
from project.processes.api.serializers import GetLastProcessInfoSerializer, RunProcessSerializer
from project.processes.models import Process, ProcessTrigger, ProcessTriggerMessage
from project.processes.tasks import run_workers
import secrets
from faker import Faker

from project.workers.consts import ParentWorker

_faker = Faker(['ru_RU'])


class ProcessViewSet(ViewSet, ResponseHandlerMixin):
    permission_classes = (IsAuthenticated, )

    @log_viewset_method()
    def list_last_process_messages(self, request: Request):
        serializer = GetLastProcessInfoSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        process = Process.objects.filter(
            scenario_id=serializer.validated_data.get("scenario_id"),
            scenario__owner=request.user
        ).order_by('-created_at').first()

        if not process:
            return self.success_response(
                body={
                    "list": [],
                    "is_completed": True,
                    "process_id": None,
                    "process_code": None
                }
            )

        triggers = ProcessTrigger.objects.filter(
            process_id=process.pk
        )

        messages = ProcessTriggerMessage.objects.filter(
            trigger__in=triggers
        )

        return self.success_response(
            body={
                "items": self._prepare_messages(messages),
                "is_completed": process.is_completed,
                "process_id": process.pk,
                "process_code": process.code
            }
        )

    @log_viewset_method()
    def run_process(self, request: Request):
        serializer = RunProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        process_code = f"{secrets.token_urlsafe(8)}_{_faker.name()}_{secrets.token_urlsafe(8)}"
        process_code = transliterate.translit(process_code, "ru", reversed=True)
        process_code = slugify(process_code)

        active_processes = Process.objects.filter(
            scenario_id=serializer.validated_data.get("scenario_id"),
            owner=request.user,
            is_completed=False
        )

        if active_processes:
            active_process = active_processes.first()
            return self.success_response(
                body={
                    "scenario_id": serializer.validated_data.get("scenario_id"),
                    "process_id": active_process.pk,
                    "process_code": active_process.code
                }
            )

        process = Process.objects.create(
            scenario_id=serializer.validated_data.get("scenario_id"),
            owner=request.user,
            code=process_code
        )

        run_workers.apply_async(
            kwargs={
                "process_id": process.id,
                "scenario_id": serializer.validated_data.get("scenario_id")
            }
        )

        return self.success_response(
            body={
                "scenario_id": serializer.validated_data.get("scenario_id"),
                "process_id": process.pk,
                "process_code": process_code
            }
        )

    def _prepare_messages(self, messages: QuerySet[ProcessTriggerMessage]):
        result = []

        result_map = {
            ParentWorker.APPLICATION.value: {
                "info": [],
                "exploit": []
            },
            ParentWorker.NETWORK.value: {
                "info": [],
                "exploit": []
            },
            ParentWorker.SCANNER.value: {
                "info": [],
                "exploit": []
            },
            ParentWorker.EXPLOIT.value: {
                "info": []
            }
        }
        for message in messages:
            value = message.value
            try:
                value = json.loads(value)
            except:
                pass

            if isinstance(value, dict):
                if "parent" in value:
                    if value.get("type") == "instruction":
                        if isinstance(value.get("result"), (list, tuple)):
                            result_map[value.get("parent")]["info"].extend(
                                value.get("result")
                            )
                        if isinstance(value.get("result"), dict):
                            result_map[value.get("parent")]["info"].append(
                                value.get("result")
                            )
                    if value.get("type") == "expoit":
                        if isinstance(value.get("result"), (list, tuple)):
                            result_map[value.get("parent")]["exploit"].extend(
                                value.get("result")
                            )
                        if isinstance(value.get("result"), dict):
                            result_map[value.get("parent")]["exploit"].append(
                                value.get("result")
                            )
                else:
                    result_map[ParentWorker.EXPLOIT.value]["info"].append(value)
            else:
                result_map[value.get("parent")]["info"].append(value)

            result.append(
                {
                    "id": message.pk,
                    "value": value,
                    "created_at": message.created_at.strftime("%d.%m.%Y %H:%S")
                }
            )

        return result_map




