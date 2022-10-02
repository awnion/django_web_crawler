from enum import IntEnum, unique
from django.db import models

from .tasks import crawl


class Crawl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    initial_url = models.URLField()

    class Status(IntEnum):
        PREPARE = 0
        RUN = 1
        PAUSE = 2
        DONE = 3

    status = models.IntegerField(default=0, choices=[(s.value, s.name) for s in Status])

    class Strategy(IntEnum):
        DEFAULT = 0
        # BFS
        # DFS
        # treat query params as unimportant or custom strategy like ?page_id=123
        # etc

    strategy = models.IntegerField(
        default=0, choices=[(s.value, s.name) for s in Strategy]
    )

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        crawl.delay(self.initial_url)
        return res


class Page(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    url = models.URLField(unique=True)
    content_hash = models.TextField(unique=True)
