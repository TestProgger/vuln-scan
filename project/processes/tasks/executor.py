from config.celery import app as celery_app
from project.workers.scanner.port_scan import PortScanner
from project.workers.scanner.nse_scan import NseScan


@celery_app.task()
def execute_command(**kwargs):
    print(f"{kwargs=}")
    try:
        result = NseScan().handle(target="192.168.109.0/24", script="*vuln*")

        print(result)

        # res = subprocess.run(
        #     args=["nmap", "192.168.109.0/24", "-vvvvv"],
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
    except Exception as ex:
        print(ex)
        return
    stdout = res.stdout.decode('utf-8').split('\n')
    print(f"{stdout=}")
    print(f"{res.stderr=}")