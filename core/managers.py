from django.db import models


class ManagerMain(models.Manager):
    def get_queryset(self, **kwargs):
        return super(ManagerMain, self).get_queryset() \
            .filter(deleted_at__isnull=True, **kwargs)


class ManagerAllMain(models.Manager):
    def get_queryset(self):
        return super(ManagerAllMain, self).get_queryset()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = ManagerMain()
    objects_all = ManagerAllMain()

    class Meta:
        abstract = True