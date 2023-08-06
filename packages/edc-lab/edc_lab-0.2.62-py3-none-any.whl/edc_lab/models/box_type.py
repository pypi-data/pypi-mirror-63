from django.db import models
from edc_model.models import BaseUuidModel

from ..constants import FILL_ACROSS
from ..choices import FILL_ORDER


class BoxTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class BoxType(BaseUuidModel):

    name = models.CharField(
        max_length=25, unique=True, help_text="a unique name to describe this box type"
    )

    across = models.IntegerField(
        help_text="number of cells in a row counting from left to right"
    )

    down = models.IntegerField(
        help_text="number of cells in a column counting from top to bottom"
    )

    total = models.IntegerField(help_text="total number of cells in this box type")

    fill_order = models.CharField(
        max_length=15, default=FILL_ACROSS, choices=FILL_ORDER
    )

    objects = BoxTypeManager()

    def __str__(self):
        return f"{self.name} max={self.total}"

    def natural_key(self):
        return (self.name,)

    class Meta:
        app_label = "edc_lab"
        ordering = ("name",)
