# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class AccountRequest(models.Model):
  """
  A request to get an account
  """
  first_name = models.CharField(_('first name'), max_length=30)
  last_name = models.CharField(_('last name'), max_length=30)
  email = models.EmailField(_('e-mail address'))
  
  pending = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return u'{0} {1}: {2}'.format(self.first_name, self.last_name, self.email)