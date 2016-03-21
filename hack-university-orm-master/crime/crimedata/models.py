# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Crimedataraw(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    recordid = models.IntegerField(db_column='RecordID', blank=True, null=True)  # Field name made lowercase.
    reportdate = models.DateField(db_column='ReportDate', blank=True, null=True)  # Field name made lowercase.
    reporttime = models.TimeField(db_column='ReportTime', blank=True, null=True)  # Field name made lowercase.
    majoroffensetype = models.CharField(db_column='MajorOffenseType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    neighborhood = models.CharField(db_column='Neighborhood', max_length=255, blank=True, null=True)  # Field name made lowercase.
    policeprecinct = models.CharField(db_column='PolicePrecinct', max_length=255, blank=True, null=True)  # Field name made lowercase.
    policedistrict = models.CharField(db_column='PoliceDistrict', max_length=255, blank=True, null=True)  # Field name made lowercase.
    xcoordinate = models.FloatField(blank=True, null=True)
    ycoordinate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crimedataraw'

    def __unicode__(self):
        """Repr."""
        return u'{self.recordid} - {self.reportdate} - {self.majoroffensetype} {self.address}'.format(self=self)
