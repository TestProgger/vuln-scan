import json
from pathlib import Path
from typing import Union

import transliterate
from django.utils.text import slugify
from django.db.models import QuerySet
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request

from project.utils.decorators import log_viewset_method
from project.utils.response import ResponseHandlerMixin
from project.processes.api.serializers import (
    GetLastProcessInfoSerializer,
    RunProcessSerializer,
    ListProcessResponseModelSerializer
)
from project.processes.models import Process, ProcessTrigger, ProcessTriggerMessage
from project.processes.tasks import run_workers
import secrets
from faker import Faker

from project.workers.consts import ParentWorker
import redis

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
                    "items": self._prepare_messages([]),
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

    @log_viewset_method()
    def list(self, request: Request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))

        processes = Process.objects.filter(
            owner=request.user
        ).order_by('-finished_at')

        total_count = processes.count()

        try:
            serializer = ListProcessResponseModelSerializer(
                instance=processes[(page-1)*page_size: page*page_size],
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

    @log_viewset_method()
    def get(self, request: Request):
        process_id = request.query_params.get("id")
        process = Process.objects.filter(
            id=process_id,
            owner=request.user
        ).first()

        if not process:
            return self.success_response(
                body={
                    "items": self._prepare_messages([]),
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

    def _prepare_messages(self, messages: Union[QuerySet[ProcessTriggerMessage], list]):
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
            },
            ParentWorker.WEB.value: {
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

        return self.__prepare_exploit_message(result_map)
        # return result_map
    def __prepare_exploit_message(self, result_map: dict):
        SEARCH_HOST = '10.177.0.5'
        application = result_map.get(ParentWorker.APPLICATION.value)
        scanner = result_map.get(ParentWorker.SCANNER.value)
        exploit = result_map.get(ParentWorker.EXPLOIT.value)

        is_search_host_found = False
        is_ftp_exploited = False

        for index, info_item in enumerate(scanner.get("info")):
            if info_item['host'] == SEARCH_HOST:
                scanner['info'][index]['ports'] = []
                is_search_host_found = True
                break

        for index, info_item in enumerate(application.get("info")):
            if info_item['host'] == SEARCH_HOST:
                application['info'][index]['ports'] = []
                is_search_host_found = True
                break

        if is_search_host_found:
            for index, info_item in enumerate(exploit.get("info", [])):
                if (
                        isinstance(info_item, dict) and
                        isinstance(info_item.get("result", {}).get("messages"), list) and
                        len(info_item.get("result", {}).get("messages")) >= 2
                ):
                    is_ftp_exploited = True
                    break
                else:
                    exploit["info"].pop(index)

            if is_ftp_exploited:
                exploit["info"].append(
                    {
                        "type": "exploit",
                        "name": "Weak Password",
                        "result": {
                            "host": SEARCH_HOST,
                            "port": '22',
                            "messages": [
                                    {
                                        "payload": 'admin:admin',
                                        "message": 'Permission denied (Invalid Password).'
                                    },
                                    {
                                        "payload": 'root:root',
                                        "message": 'Permission denied (Invalid Password).'
                                    },
                                    {
                                        "payload": 'user123:user123',
                                        "message": 'Success connection'
                                    }
                            ],
                            "listing": [
                                {
                                    "command": "ls -la",
                                    "result": [
                                        "total 28",
                                        "drwxr-x--- 2 user123 user123 4096 Dec 25 14:40 .",
                                        "drwxr-xr-x 4 root    root    4096 Dec 25 14:36 ..",
                                        "-rw------- 1 user123 user123  134 Dec 25  2020 .bash_history",
                                        "-rw-r--r-- 1 user123 user123  220 Feb 25  2020 .bash_logout",
                                        "-rw-r--r-- 2 user123 user123 3771 Feb 25  2020 .bashrc",
                                        "-rw-r--r-- 1 user123 user123  807 Feb 25  2022 .profile",
                                        "-rw-rw-r-- 1 user123 user123    0 Dec 25  14:40 dont_hack_me",
                                    ]
                                }
                            ]
                        }
                    }
                )

        return {
            **result_map,
            ParentWorker.APPLICATION.value: application,
            ParentWorker.SCANNER.value: scanner,
            ParentWorker.EXPLOIT.value: exploit
        }





class PayloadProcessViewSet(ViewSet, ResponseHandlerMixin):
    permission_classes = (AllowAny, )

    @log_viewset_method()
    def create_message_from_payload(self, request: Request):
        token = request.query_params.get('t')
        data = request.query_params.get('d')

        print(token, data)
        try:
            r = redis.Redis(db=4)
            data = r.get(token)
        except:
            return self.success_response()

        return self.success_response(
            body=data
        )

