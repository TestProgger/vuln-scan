from project.workers.base import Manager

# ============================
# WORKERS
# ============================
from project.workers.application import *
from project.workers.web import *
from project.workers.scanner import *


worker_manager = Manager()
