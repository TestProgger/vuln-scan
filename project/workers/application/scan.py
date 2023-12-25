import os
from project.workers.base import BaseWorker
from project.workers.scanner.consts import NmapScriptKey, NmapTableElemKey
from project.workers.application.consts import WorkersNames
from project.workers.consts import ParentWorker
from project.workers.scanner.serializers import NseScannerSerializer
from django.conf import settings
import subprocess
from uuid import uuid4
from bs4 import BeautifulSoup
import socket


class Scan(BaseWorker):
    parent = ParentWorker.APPLICATION.value
    name = WorkersNames.SCAN.value
    serializer = NseScannerSerializer
    self_ip = socket.gethostbyname(socket.gethostname())

    def run(self):
        file_name = str(settings.BASE_DIR / f"{str(uuid4())}.xml")
        try:
            proc = subprocess.run(
                args=[
                    "nmap",
                    "-sV",
                    "-T4",
                    "-O",
                    "--min-parallelism", "64",
                    "--script", self.serialized_data.get("script"),
                    self.serialized_data.get("target"),
                    "-oX", file_name,
                    "--top-ports", "2000"
                ],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
        except Exception as ex:
            raise
        # else:
        #     if proc.returncode != 0:
        #         raise Exception(proc.stderr.decode("utf-8"))

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

            try:
                host_status = host_tag.find("status").get("state")
            except:
                host_status = "up"
            try:
                ip_address = host_tag.find("address", addrtype="ipv4").get("addr")
                if ip_address == settings.CURRENT_HOST_IP:
                    continue
            except:
                continue
            try:
                mac_address = host_tag.find("address", addrtype="mac").get("addr")
            except:
                mac_address = None

            result_dict.update(
                {
                    "host": ip_address,
                    "os": self.__extract_os(host_tag),
                    "mac": mac_address,
                    "status": host_status,
                    "ports": []
                }
            )

            host_ports_tag = host_tag.find("ports")

            host_ports = host_ports_tag.find_all("port")

            for host_port in host_ports:
                try:
                    port_state = host_port.find("state").get("state")
                    service_name = host_port.find("service").get("name") if host_port.find("service") else None
                    port_scripts = host_port.find_all("script")
                except:
                    continue

                try:
                    service_product = host_port.find("service").get("product") if host_port.find("service") else None
                    service_version = host_port.find("service").get("version") if host_port.find("service") else None
                except:
                    service_product = None
                    service_version = None
                    pass
                port_result_dict = {
                    "host": ip_address,
                    "mac": mac_address,
                    "port": host_port.get("portid"),
                    "protocol": host_port.get("protocol"),
                    "state": port_state,
                    "service": {
                        "name": service_name,
                        "product": service_product,
                        "version": service_version
                    },
                    "vulns": []
                }
                try:
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
                except:
                    pass
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

    def __extract_os(self, host):
        try:
            os = host.find("os")
            os_matches = os.find_all("osmatch") or []
            for os_match in os_matches:
                try:
                    os_family = os_match.find("osclass").get("osfamily")
                    if os_family.lower() in ("windows", "linux", "nt", "android", "bsd"):
                        return os_family
                except:
                    continue
        except:
            pass

        return "Linux"