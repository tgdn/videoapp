# -*- coding: utf-8 -*-

#   Copyright (c) 2013, Thomas Gak Deluen. See
#   the COPYRIGHT file.

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from mysite.main.models import AccountRequest


class AccountRequestForm(forms.ModelForm):
  
  class Meta:
    model = AccountRequest
    fields = ('first_name', 'last_name', 'email',)
    
  def clean_email(self):
    email = self.cleaned_data['email']
    try:
      User.objects.get(email=email)
    except User.DoesNotExist:
      try:
        AccountRequest.objects.get(email=email)
      except AccountRequest.DoesNotExist:
        return email
    raise forms.ValidationError(_('Email address already taken'))


# TODO

#class ContactForm(forms.ModelForm):
#  
#  class Meta:
#    model = ContactMessage