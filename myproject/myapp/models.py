# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Message(models.Model):
	sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	recipient = models.CharField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	send_date = models.DateTimeField(default=timezone.now)
	

	def send(self):
		self.send_date = timezone.now()
		self.save()

	def __str__(self):
		return self.subject