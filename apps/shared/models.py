from django.db import models


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")

    class Meta:
        abstract = True
