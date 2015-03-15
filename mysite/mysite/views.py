# -*- coding: utf-8 -*-

#   Copyright (c) 2013, Thomas Gak Deluen. See
#   the COPYRIGHT file.

from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm

from annoying.decorators import render_to


@csrf_protect
@render_to('templates/main/home.html')
def home(request):
  page_id = 'home'
  title = _('Home')
  return locals()