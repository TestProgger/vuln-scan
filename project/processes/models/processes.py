from django.db import models
from project.utils.models import AbstractDictionaryModel, AbstractCreatedUpdateBaseModel
from django.contrib.auth.models import User


class ProcessStatus(AbstractDictionaryModel):
    class Meta:
        db_table = "process_status"


class Process(AbstractCreatedUpdateBaseModel):
    scenario = models.ForeignKey("scenarios.Scenario", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey("processes.ProcessStatus", on_delete=models.RESTRICT, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    class Meta:
        db_table = "process"


class ProcessMessage(AbstractCreatedUpdateBaseModel):
    process = models.ForeignKey("processes.Process", on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "process_message"

