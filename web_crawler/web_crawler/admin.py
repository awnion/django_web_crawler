from django.contrib import admin

from .models import *


@admin.register(Crawl)
class CrawlAdmin(admin.ModelAdmin):
    list_display = ['initial_url', 'created_at', 'updated_at']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['url', 'content_hash', 'created_at', 'updated_at']
