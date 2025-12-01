
from django.db import models
from django.db.models.functions import Now
from django.conf import settings
from django.utils import timezone


from apps.abstracts.models import AbstractSoftDeletableModel
from apps.auths.models import CustomUser
from decimal import Decimal



class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=Now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.exclude(deleted_at__isnull=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)



class Course(models.Model):
    TITLE_MAX_LEMGTH = 200
    DESCRIPTION_MAX_LENGTH = 2000

    title = models.CharField(
        max_length=TITLE_MAX_LEMGTH,
        db_index = True,
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        default='',
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    owner = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses',
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
        default=None,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-created_at']
    
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])





class Lesson(models.Model):
    TITLE_MAX_LENGTH = 200

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        db_index=True,
    )

    content = models.TextField()

    indentation = models.PositiveIntegerField(
        default=0,
    )

    order = models.DecimalField(
        max_digits=12,
        decimal_places=7,
    )

    is_published = models.BooleanField(
        default=False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()  

    class Meta:
        ordering = ['order']


    def save(self, *args, **kwargs):
        if not self.pk:
            first = (
                Lesson.all_objects.filter(course=self.course,deleted_at__isnull=True)
                .order_by('-order')
                .first()
            )
            if first:
                self.order = Decimal(0)
            else:
                self.order = Decimal(first.order) - Decimal(1)

            if self.indentation is None:
                self.indentation = 0
            if self.indentation > 5:
                self.indentation = 5
        super().save(*args, **kwargs)


    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def __str__(self):
        return f"{self.title} (Course: {self.course.title})"


