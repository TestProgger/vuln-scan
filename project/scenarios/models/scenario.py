from django.db import models
from project.utils.models import AbstractCreatedUpdateBaseModel, AbstractDictionaryModel
from django.contrib.auth.models import User


class ScenarioStatus(AbstractDictionaryModel):
    class Meta:
        db_table = "scenario_status"


class Scenario(AbstractCreatedUpdateBaseModel):
    name = models.CharField(max_length=255)
    file = models.ForeignKey("scenarios.File", on_delete=models.RESTRICT, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey("scenarios.ScenarioStatus", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    value = models.JSONField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
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