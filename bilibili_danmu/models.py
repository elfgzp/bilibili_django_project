# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from datetime import datetime
from django.utils import timezone
import time


class IntegerTimeField(models.TimeField):
    description = 'Convert Integer to Datetime Field'

    def get_prep_value(self, value):
        if value is None:
            return None
        try:
            return int(time.mktime(value.timetuple()))
        except (TypeError, ValueError):
            raise ValidationError("This object must be an datetime.")

    def to_python(self, value):
        if isinstance(value, timezone.datetime):
            return value
        if value is None:
            return None
        try:
            return datetime.fromtimestamp(value)
        except (TypeError, ValueError):
            raise ValidationError("This value must be an integer or a float.")

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SplitDateTimeField, 'widget': widgets.AdminSplitDateTime, 'required': False}
        defaults.update(kwargs)
        return super(IntegerTimeField, self).formfield(**defaults)


class Rooms(models.Model):
    url = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'rooms'


class Ss234024(models.Model):
    number = models.IntegerField(blank=True, null=True)
    time = IntegerTimeField(blank=True, null=True)

    class Meta:
        db_table = 'ss234024'


class Tt234024(models.Model):
    uid = models.IntegerField(blank=True, null=True, verbose_name='B站UID', db_index=True)
    name = models.TextField(blank=True, null=True, verbose_name='B站ID', db_index=True)  # This field type is a guess.
    comment = models.TextField(blank=True, null=True, verbose_name='弹幕', db_index=True)
    time = IntegerTimeField(blank=True, null=True, verbose_name='时间', db_index=True)

    class Meta:
        db_table = 'tt234024'
        verbose_name = '弹幕统计'
        verbose_name_plural = '弹幕统计'

    def __unicode__(self):
        return '{}: {}'.format(self.name, self.comment)
