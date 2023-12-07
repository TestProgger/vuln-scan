from project.workers.consts import ParentWorker
from project.workers.web.consts import WorkerNames
from project.workers.web.serializers import SqlInjectionSerializer
from project.workers.base import BaseWorker
import subprocess


class SqlInjectionWorker(BaseWorker):
    parent = ParentWorker.WEB.value
    name = WorkerNames.SQL_INJECTION.value
    serializer = SqlInjectionSerializer

    def run(self):
        process = subprocess.run(
            args=[
                "sqlmap", "-u", self.serialized_data.get("target"),
                "-a", "--batch", "--dump-all", "--random-agent"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode != 0:
            raise Exception(process.stderr.decode("utf-8"))

        return {"message":  process.stdout.decode("utf-8")}

    def format(self, **kwargs):
        return kwargs

