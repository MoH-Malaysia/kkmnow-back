import jsonfield
import datetime
from django.db import models
from django.utils import timezone

class MetaJson(models.Model) :
    dashboard_name = models.CharField(max_length=200)
    dashboard_meta = models.JSONField()

class KKMNowJSON(models.Model) :
    dashboard_name = models.CharField(max_length=200)
    chart_name = models.CharField(max_length=200, null=True)
    chart_type = models.CharField(max_length=200, null=True)
    api_type = models.CharField(max_length=200, null=True)
    chart_data = models.JSONField()

class GitHashData(models.Model) :
    index = models.CharField(max_length=200, default='HASH_DATA')
    last_update = models.DateTimeField(default=timezone.now,blank=True)
    git_hash = models.CharField(max_length=200)