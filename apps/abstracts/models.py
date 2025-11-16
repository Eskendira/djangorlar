from typing import Any
from django.db.models import Model, DateTimeField
from django.utils import timezone as django_timezone


class AbstractSoftDeletableModel(Model):
    created_at = DateTimeField(
        auto_now_add=True
    )
    updated_at = DateTimeField(
        auto_now=True
    )
    deleted_at = DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        self.deleted_at = django_timezone.now()
        self.save(update_fields=["deleted_at"])