from project.workers.base import Manager

# ============================
# WORKERS
# ============================
from project.workers.application import *
from project.workers.web import *


worker_manager = Manager()
