import os

from project.workers.base import BaseWorker
from project.workers.scanner.consts import PARENT_NAME, HandlersNames
from project.workers.scanner.serializers import NseScannerSerializer
import nmap3
from django.conf import settings
import subprocess
from uuid import uuid4
from xml.dom import minidom
from bs4 import BeautifulSoup


class NseScan(BaseWorker):
    parent = PARENT_NAME
    name = HandlersNames.NSE_SCANNER.value
    serializer = NseScannerSerializer
    nmap = nmap3.Nmap()

    def run(self):
        file_name = str(settings.BASE_DIR / f"{str(uuid4())}.xml")
        try:
            proc = subprocess.run(
                args=[
                    "nmap",
                    "--script",
                    self.serialized_data.get("script"),
                    self.serialized_data.get("target"),
                    "-oX",
                    file_name
                ],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
        except Exception as ex:
            raise
        else:
            if proc.returncode != 0:
                raise Exception(proc.stderr.decode("utf-8"))

        return {"file_name": file_name}

    def format(self, **kwargs):
        file_name = kwargs.get("file_name")
        with open(file_name) as fr:
            parser = BeautifulSoup(fr.read(), "xml")
        os.remove(file_name)
        host_tags = parser.find_all("host")

        result = []
        for host_tag in host_tags:
            result_dict = {}

            host_status = host_tag.find("status").get("state")
            address = host_tag.find("address").get("addr")
            result_dict.update(
                {
                    "host": address,
                    "status": host_status,
                    "ports": []
                }
            )

            host_ports_tag = host_tag.find("ports")

            host_ports = host_ports_tag.find_all("port")

            for host_port in host_ports:

                port_state = host_port.find("state").get("state")
                port_service = host_port.find("service").get("name")
                port_scripts = host_port.find_all("script")

                port_result_dict = {
                    "port": host_port.get("portid"),
                    "protocol": host_port.get("protocol"),
                    "state": port_state,
                    "service": port_service,
                    "vulns": []
                }
                for port_script in port_scripts:
                    output = port_script.get("output")
                    if output.strip().startswith("ERROR"):
                        continue
                    tables = port_script.find("table")
                    if not tables:
                        continue
                    tables = tables.find_all("table")

                    for table in tables:
                        if table.get("key") == "ids":
                            port_result_dict["vulns"].append(
                                table.find("elem").text
                            )
                result_dict["ports"].append(port_result_dict)

            result.append(result_dict)

        return result
