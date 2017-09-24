# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# from djangotoolbox.fields import ListField


# class Locale(models.Model):
#     name = models.CharField(max_length=55)
#     lat = models.CharField(max_length=12)
#     lon = models.CharField(max_length=12)
#     avg = models.DecimalField(decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Report(models.Model):
#     locale = models.ForeignKey('Locale', on_delete=models.CASCADE)
#     count = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
