from django.db import models
from project.utils.models.mixins import PkUUIDModelMixin, DictionaryModelMixin
from uuid import uuid4

class AbstractBaseModel(models.Model, PkUUIDModelMixin):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid4,
        verbose_name="ID"
    )

    class Meta:
        abstract = True


class AbstractDictionaryModel(AbstractBaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    code = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class AbstractCreatedUpdateBaseModel(AbstractBaseModel):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
