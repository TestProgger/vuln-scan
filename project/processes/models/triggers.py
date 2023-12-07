from project.utils.models import AbstractCreatedUpdateBaseModel
from django.db import models


class ProcessTrigger(AbstractCreatedUpdateBaseModel):
    process = models.ForeignKey("processes.Process", on_delete=models.CASCADE)
    scenario_block = models.ForeignKey("scenarios.ScenarioBlock", on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "process_trigger"


class ProcessTriggerMessage(AbstractCreatedUpdateBaseModel):
    trigger = models.ForeignKey("processes.ProcessTrigger", on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "process_trigger_message"
