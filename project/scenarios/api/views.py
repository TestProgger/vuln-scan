from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
import base64
import yaml

from project.processes.tasks import run_workers
from project.scenarios.models import Scenario, ScenarioBlock
from project.processes.models import Process
from project.workers.consts import ParentWorker
from project.workers.manager import worker_manager
from faker import Faker

from project.workers.os.exploit.vsftpd_cve_2011_2523 import VsftpdExploit

_faker = Faker()


class ScenarioViewSet(ViewSet):
    permission_classes = (AllowAny, )

    def upload(self, request: Request):
        file = request.data.get("file")
        decoded_file = base64.b64decode(file).decode("utf-8")
        yaml_dict = yaml.load(decoded_file, yaml.FullLoader)

        if yaml_dict.get("version") != '1.0':
            return Response(data={"message": "Не поддерживаемая версия языка"}, status=400)

        if not yaml_dict.get("services"):
            return Response(data={"message": "Не найдено инструкций для исполнения"}, status=400)

        name = _faker.unique.name()
        sc = Scenario.objects.create(
            name=name,
            value=yaml_dict
        )

        services = yaml_dict.get("services", {})

        for key, value in services.items():
            if key not in (
                ParentWorker.WEB.value,
                ParentWorker.NETWORK.value,
                ParentWorker.SCANNER.value,
                ParentWorker.OS.value
            ):
                return Response(data={"message": f"Неизвестная инструкция {key}"}, status=400)

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

        return Response(data={"scenario_id": sc.pk, "name": name})

    def run_scenario(self, request: Request):
        scenario_id = request.data.get("scenario_id")
        process = Process.objects.create(scenario_id=scenario_id)

        run_workers.apply_async(
            kwargs={"process_id": process.id, "scenario_id": scenario_id}
        )

        return Response(data={"scenario_id": scenario_id, "process_id": process.pk})
