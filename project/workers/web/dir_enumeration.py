from project.workers.consts import ParentWorker
from project.workers.web.consts import WorkerNames
from project.workers.base import BaseWorker
from project.workers.web.serializers import DirEnumerationSerializer
from django.conf import settings
import subprocess


class DirEnumerationWorker(BaseWorker):
    parent = ParentWorker.WEB.value
    name = WorkerNames.HTTP_ENUM.value
    serializer = DirEnumerationSerializer

    wordlist = settings.BASE_DIR / "project" / "workers" / "web" / "wordlists" / "common.txt"

    def run(self):
        process = subprocess.run(
            args=[
                "gobuster",
                "-t", "20",
                "-u", self.serialized_data.get("target"),
                "-w", str(self.wordlist),
                "--hide-length",
                "--status-codes", "200,201,300,301",
                "--status-codes-blacklist", "\"\""
            ],

            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(process.stdout.decode("utf-8"))
        if process.returncode != 0:
            raise Exception(process.stderr.decode("utf-8"))

        return {"message": process.stdout.decode("utf-8")}
