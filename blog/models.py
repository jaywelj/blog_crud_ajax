# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date = models.DateField(default=timezone.now)
	published_date = models.DateField(null=True, blank=True)

	def publish(self):
		self.published_date = timezone.now()


	def __str__(self):
		return self.title


