# -*- coding: utf-8 -*-

import json

from django.contrib import admin
from bilibili_danmu import models
import bilibili_danmu.filter as filter
from django.conf.urls import url
from django.http import HttpResponse


# Register your models here.

@admin.register(models.Tt234024)
class Tt234024Admin(admin.ModelAdmin):
    class Media:
        js = ('http://lib.sinaapp.com/js/jquery/1.9.1/jquery-1.9.1.min.js',
              '/static/js/change_list.js',)

    fields = ('id', 'name', 'comment', 'time')
    readonly_fields = ('id', 'name', 'comment', 'time')
    list_display = ('id', 'name', 'comment', 'time')
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'comment')

    list_filter = (('time', filter.DateTimeRangeFilter),)

    def get_data(self, request, id):
        last_id = int(id)
        new_last_id = models.Tt234024.objects.order_by('-id').first().id
        if new_last_id > last_id:
            new_records = models.Tt234024.objects.all()[last_id: new_last_id]
            res = [{'id': each_record.id,
                    'name': each_record.name,
                    'comment': each_record.comment,
                    'time': each_record.time.strftime('%Y年%-m月%-d日 %H:%M')}
                   for each_record in new_records]
            return HttpResponse(json.dumps(res))

        return HttpResponse(json.dumps({}))

    def get_urls(self):
        urls = super(Tt234024Admin, self).get_urls()
        my_urls = [
            url(r'^(.+)/change/ajax/get_data/$',
                self.admin_site.admin_view(self.get_data), name='get_data'),
        ]
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['extra_var'] = 'Hello World'
        return super(Tt234024Admin, self).changelist_view(request, extra_context)


admin.site.site_header = 'bilibili264弹幕统计'
admin.site.site_title = 'bilibili264弹幕统计'
admin.site.index_title = 'bilibili264弹幕统计'
