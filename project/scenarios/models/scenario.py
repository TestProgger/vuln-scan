from django.db import models
from project.utils.models import AbstractCreatedUpdateBaseModel, AbstractDictionaryModel
from django.contrib.auth.models import User


class ScenarioStatus(AbstractDictionaryModel):
    class Meta:
        db_table = "scenario_status"


class Scenario(AbstractCreatedUpdateBaseModel):
    name = models.CharField(max_length=255)
    file = models.ForeignKey("scenarios.File", on_delete=models.RESTRICT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey("scenarios.ScenarioStatus", on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "scenario"


class ScenarioBlock(AbstractCreatedUpdateBaseModel):
    scenario = models.ForeignKey("scenarios.Scenario", on_delete=models.CASCADE)
    value = models.JSONField()
    depend_on = models.ForeignKey("scenarios.ScenarioBlock", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "scenario_block"