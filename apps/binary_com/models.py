from django.db import models

class Players(models.Model):
  token = models.CharField(max_length=255, blank=True, null=True, db_index=True)

