# -*- coding: utf-8 -*-

#   Copyright (c) 2013, Thomas Gak Deluen. See
#   the COPYRIGHT file.

import urllib
import requests
from django.conf import settings

# thank you http://mymovieapi.com/

DEFAULT_URL = 'http://mymovieapi.com'
DEFAULT_PARAMS = { 'type': 'json', 'plot': 'simple', 'episode': 1, 'limit': 1, 'yg': 0, 'mt': 'none', 'lang': 'en-US', 'offset': '', 'aka': 'simple', 'release': 'simple', 'business': 0, 'tech': 0 }

def log_message(message):
  if getattr(settings, 'DEBUG', False):
    print >>sys.stderr, message
    

def build_url(**kwargs):
  args = DEFAULT_PARAMS
  for name, value in kwargs.items():
    args[name] = value
  
  url_args = urllib.urlencode(args)
  url = '{0}/?{1}'.format(DEFAULT_URL, url_args)
  
  return url

def build_request(url):
  try:
    log_message('Retrieving IMDb data from: %s' % url)
    r = requests.get(url)
    log_message('Successfully fetched data')
  except requests.ConnectionError:
    log_message('Failed accessing: %s' % url)
    return None
  return r

def get_imdb_info_from_title(title):
  """
  Retrieve movie info from IMDb depending on movie title
  """
  url = build_url(title=title)
  r = build_request(url)
  
  try:
    j = r.json()
  except:
    return None
  return j

def get_imdb_info_from_id(_id):
  """
  Retrieve movie info from IMDb depending on IMDb movie id
  """
  url = build_url(id=_id)
  r = build_request(url)
  
  try:
    j = r.json()
  except:
    return None
  return j