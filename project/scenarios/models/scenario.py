from django.db import models
from project.utils.models import AbstractCreatedUpdateBaseModel, AbstractDictionaryModel
from django.conf import settings


class ScenarioStatus(AbstractDictionaryModel):
    class Meta:
        db_table = "scenario_status"


class Scenario(AbstractCreatedUpdateBaseModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.ForeignKey("scenarios.ScenarioStatus", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    text = models.TextField()
    value = models.JSONField()
    hashsum = models.CharField(max_length=130)
    type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ["owner", "hashsum"]
        db_table = "scenario"


class ScenarioBlock(AbstractCreatedUpdateBaseModel):
    scenario = models.ForeignKey("scenarios.Scenario", on_delete=models.CASCADE)
    instruction = models.CharField(max_length=255, null=True,blank=True)
    parent_instruction = models.CharField(max_length=255, null=True,blank=True)
    value = models.JSONField()
    depend_on = models.ForeignKey("scenarios.ScenarioBlock", on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True, blank=True, related_name="childs")

    class Meta:
        db_table = "scenario_block"