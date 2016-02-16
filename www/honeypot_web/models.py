# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class BanAddress(models.Model):
    ip = models.TextField(primary_key=True)
    ban_date = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ban_address'


class Broker(models.Model):
    url = models.TextField()
    insert_date = models.DateTimeField(auto_now_add=True)
    schedule_date = models.DateField(blank=True, null=True)
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'broker'
