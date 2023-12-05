from project.workers.consts import ParentWorker
from project.workers.web.consts import WorkerNames
from project.workers.base import BaseWorker
from project.workers.web.serializers import DirEnumerationSerializer
from django.conf import settings
import subprocess


class DirEnumeration(BaseWorker):
    parent = ParentWorker.WEB.value
    name = WorkerNames.DIR_ENUMERATION.value
    serializer = DirEnumerationSerializer

    wordlist = settings.BASE_DIR / "projects" / "workers" / "web" / "wordlists" / "common.txt"

    def run(self):
        process = subprocess.run(
            args=["dirb", self.serialized_data.get("target"), str(self.wordlist)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode != 0:
            raise Exception(process.stderr.decode("utf-8"))

        return {"result": process.stdout.decode("utf-8")}
