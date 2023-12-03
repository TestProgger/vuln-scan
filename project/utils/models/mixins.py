from django.db import models
from uuid import uuid4


class PkUUIDModelMixin:
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid4,
        verbose_name="ID"
    )

    class Meta:
        abstract = True


class DictionaryModelMixin:
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


class CreatedUpdatedModelMixin:
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )