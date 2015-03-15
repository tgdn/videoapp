# -*- coding: utf-8 -*-

#   Copyright (c) 2013, Thomas Gak Deluen. See
#   the COPYRIGHT file.

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm

from annoying.decorators import render_to

from videostream.models import VideoCategory, Video

from mysite.main.forms import AccountRequestForm


@login_required
@csrf_protect
@render_to('templates/main/home.html')
def home(request):
  page = 'home'
  title = _('Home')
  latest = Video.objects.filter(is_public=True)
  return locals()


@csrf_protect
@render_to('templates/main/request_pass.html')
def request_pass(request):
  page = 'request'
  title = _('Request an account')
  
  form = AccountRequestForm(request.POST or None)
  if form.is_valid():
    form.save()
    del form
  
  return locals()


@login_required
@csrf_protect
@render_to('templates/main/about.html')
def about(request):
  page = 'about'
  title = _('About')
  return locals()


@login_required
@csrf_protect
@render_to('templates/main/contact.html')
def contact(request):
  page = 'contact'
  title = _('Contact us')
  return locals()


@csrf_protect
@never_cache
@render_to('templates/main/signup.html')
def signup(request):
  if request.user.is_authenticated():
    return redirect('home')
  page = 'signup'
  title = _('Sign up')
  
  ###
  ### TODO: This needs to be completed
  ###
  
  #form = SignupForm(request.POST or None)
  #if form.is_valid():
  #  form.save()
  #  return redirect('/?successfully_signed_up=1')
  return locals()
