import os

from django.db import models

class Credit(models.Model):
    credit_id = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    _range = models.CharField(max_length=300, blank=True)
    cancel_reason = models.CharField(max_length=300, blank=True)
    supposed_by = models.CharField(max_length=300, blank=True)
    taxpayer_type = models.CharField(max_length=300, blank=True)
    entity = models.CharField(max_length=300, blank=True)
    sector = models.CharField(max_length=300, blank=True)

class DataBaseFile(models.Model):
    def __unicode__(self):
        return self.title

    def file_name(self):
        return os.path.basename(self.content_file.name)

    title = models.CharField(max_length=100, verbose_name="Titulo")
    content_file = models.FileField(upload_to='.', verbose_name="Archivo")
