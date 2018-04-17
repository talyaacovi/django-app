# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, MessageForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.
def home(request):
	messages = Message.objects.all()
	return render(request, 'myapp/home.html', {'messages': messages})

def messages(request, username):
	user = get_object_or_404(User, username=username)
	messages = Message.objects.filter(Q(recipient=user.username) | Q(sender=user))
	
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			messageObj = form.cleaned_data
			subject = messageObj['subject']
			message = messageObj['message']
			sender = request.user
			send_date = timezone.now()
			recipient = 'site-admin'
			message = Message.objects.create(sender=sender, recipient=recipient, subject=subject, message=message, send_date=send_date)
			message.save()
			return redirect('/messages/' + user.username)
	else:
		form = MessageForm()
	return render(request, 'myapp/messages.html', {'messages': messages, 'form': form})


def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				User.objects.create_user(username, email, password)
				user = authenticate(username = username, password = password)
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				raise forms.ValidationError('Looks like a username with that email or password already exists')
	else:
		form = UserRegistrationForm()
	return render(request, 'myapp/register.html', {'form': form})