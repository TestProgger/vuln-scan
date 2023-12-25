from config.celery import app as celery_app
from project.workers.scanner.port_scan import PortScanner
from project.workers.scanner.nse_scan import NseScan


