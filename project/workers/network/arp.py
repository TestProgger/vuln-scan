import subprocess

from project.workers.consts import ParentWorker
from project.workers.network.consts import WorkerNames
from project.workers.base import BaseWorker
from project.workers.network.serializers import ArpPoisonSerializer


class ArpPoison(BaseWorker):
    parent = ParentWorker.NETWORK.value
    name = WorkerNames.ARP_POISONING.value
    serializer = ArpPoisonSerializer



    def run(self):
        process = subprocess.Popen(
            args=["arpspoof"]
        )
