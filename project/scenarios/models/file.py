from django.db import models
from project.utils.models import AbstractDictionaryModel, AbstractCreatedUpdateBaseModel
from django.contrib.auth.models import User


class FileProcessingStatus(AbstractDictionaryModel):
    class Meta:
        db_table = "scenario_file_processing_status"


class File(AbstractCreatedUpdateBaseModel):
    minio_etag = models.UUIDField()
    status = models.ForeignKey("scenarios.FileProcessingStatus", on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hashsum = models.CharField(max_length=256, db_index=True)

    class Meta:
        db_table = "scenario_file"


class FileProcessingErrors(AbstractDictionaryModel):
    file = models.ForeignKey("scenarios.File", on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "scenario_file_processing_errors"
