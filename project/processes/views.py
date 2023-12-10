import json

from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from project.processes.models import ProcessTriggerMessage, ProcessTrigger


class GetProcessTriggerMessageView(ViewSet):
    permission_classes = (AllowAny, )


    def get_message(self, request: Request):
        process_id = request.data.get("process_id")

        triggers = ProcessTrigger.objects.filter(
            process_id__in=[process_id]
        )

        messages = ProcessTriggerMessage.objects.filter(
            trigger__in=triggers
        )

        response = []

        for message in messages:
            value = message.value
            try:
                value = json.loads(value)
            except:
                pass

            response.append(
                {
                    "id": message.pk,
                    "value": value,
                    "created_at": message.created_at
                }
            )

        return Response(data=response)



