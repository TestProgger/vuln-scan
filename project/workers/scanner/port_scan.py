from project.workers.base import BaseWorker
from project.workers.scanner.consts import WorkersNames
from project.workers.consts import ParentWorker
from project.workers.scanner.serializers import PortScannerSerializer
import nmap3


class PortScanner(BaseWorker):
    parent = ParentWorker.SCANNER.value
    name = WorkersNames.PORT_SCANNER.value
    serializer = PortScannerSerializer
    nmap = nmap3.NmapScanTechniques()

    def run(self):
        if self.serialized_data.get("ports"):
            return self.nmap.nmap_syn_scan(self.serialized_data.get('target'), args=f"-p{self.serialized_data.get('ports')} -A")
        return self.nmap.scan_top_ports(
            self.serialized_data.get('target'), self.serialized_data.get("top_ports", 2000) or 2000
        )

    def format(self, **kwargs):
        result = []
        for key, value in kwargs.items():
            if '.' in key:
                host = kwargs[key]
                if host.get("state", {}).get("state") == "up":
                    macaddress = host.get("macaddress", {})
                    result.append(
                        {
                            "host": key,
                            "ports": self.__format_ports(host),
                            "macaddress": macaddress.get("addr") if macaddress else None
                        }
                    )

        return result

    def __format_ports(self, host: dict):
        result = []
        for port in host.get("ports", []):
            result.append(
                {
                    "port": port.get('portid'),
                    "protocol": port.get("protocol"),
                    "service_name": port.get("service", {}).get("name")
                }
            )
        return result
