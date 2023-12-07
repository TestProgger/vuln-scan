from project.workers.base import Manager

# ============================
# WORKERS
# ============================
from project.workers.os import *
from project.workers.web import *


worker_manager = Manager()
