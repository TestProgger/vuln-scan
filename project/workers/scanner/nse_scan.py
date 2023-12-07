from project.workers.base import BaseWorker
from project.workers.scanner.consts import WorkersNames, NmapScriptKey, NmapTableElemKey
from project.workers.consts import ParentWorker
from project.workers.scanner.serializers import NseScannerSerializer
from django.conf import settings
import subprocess
from uuid import uuid4
from bs4 import BeautifulSoup
import os


class NseScan(BaseWorker):
    parent = ParentWorker.SCANNER.value
    name = WorkersNames.NSE_SCANNER.value
    serializer = NseScannerSerializer

    def run(self):
        file_name = str(settings.BASE_DIR / f"{str(uuid4())}.xml")
        try:
            proc = subprocess.run(
                args=[
                    "nmap",
                    "-sV",
                    "-T4",
                    "--min-parallelism", "1024",
                    "--script", self.serialized_data.get("script"),
                    self.serialized_data.get("target"),
                    "-oX", file_name
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
                port_service = host_port.find("service").get("product")
                port_service_version = host_port.find("service").get("version")
                port_scripts = host_port.find_all("script")
                port_result_dict = {
                    "port": host_port.get("portid"),
                    "protocol": host_port.get("protocol"),
                    "state": port_state,
                    "service": {
                        "name": port_service,
                        "version": port_service_version
                    },
                    "vulns": []
                }
                for port_script in port_scripts:
                    output = port_script.get("output")
                    if "ERROR" in output.strip():
                        continue
                    tables = port_script.find("table")
                    if not tables:
                        continue
                    tables = tables.find_all("table")

                    for table in tables:
                        if table.get("key") in (
                            NmapScriptKey.IDS.value,
                            NmapScriptKey.VULNERS.value
                        ):
                            port_result_dict["vulns"].append(
                                table.find("elem").text
                            )
                        else:
                            cve_id = self.__extract_cve_ids(table)
                            if cve_id:
                                port_result_dict["vulns"].append(
                                    cve_id
                                )


                result_dict["ports"].append(port_result_dict)

            result.append(result_dict)

        return result

    def __extract_cve_ids(self, table):
        is_cve = table.find("elem", key=NmapTableElemKey.TYPE.value).text == "cve"
        if is_cve:
            return table.find("elem", key=NmapTableElemKey.ID.value).text
        is_prion = table.find("elem", key=NmapTableElemKey.TYPE.value).text == "prion"
        if is_prion:
            return table.find("elem", key=NmapTableElemKey.ID.value).text.replace("PRION:", "")
        return None