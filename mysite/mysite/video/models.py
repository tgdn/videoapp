# -*- coding: utf-8 -*-

from datetime import datetime
import sys

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from videostream.models import Video, VideoCategory
import mysite.video.utils as utils

def save_imdb_genres_from_data(data):
  genres = []
  if data.get('genres') is not None:
    for genre in data.get('genres'):
      try:
        vc = VideoCategory.objects.get(title=genre)
      except VideoCategory.DoesNotExist:
        vc = VideoCategory(title=genre, slug=slugify(genre)).save()
        del(vc)
        vc = VideoCategory.objects.get(title=genre)
      genres.append(vc)
    return genres
  return None
  

def save_imdb_data_for_video(video):
  data = utils.get_imdb_info_from_title(video.title)
  if data is None:
    return
  data = data[0]
  genres = save_imdb_genres_from_data(data)
  
  #print >>sys.stderr, '%s' % data
  info = VideoInfo(video=video, imdb_id=data.get('imdb_id'),
                   imdb_url=data.get('imdb_url'), year=data.get('year'),
                   poster=data.get('poster'), plot=data.get('plot'),
                   plot_short=data.get('plot_simple'))
  info.save()
  for genre in genres:
    video.categories.add(genre)


def update_imdb_data_for_video_from_imdb_id(video, _id):
  """
  Should only be called to update data not to create!
  """
  data = utils.get_imdb_info_from_id(_id)
  if data is None:
    return
  genres = save_imdb_genres_from_data(data)
  
  # Delete current info
  current_info = VideoInfo.objects.get(video=video)
  current_info.delete()
  
  # Create new info, because creating a new entry is faster to write
  # than to update each field one by one
  new_info = VideoInfo(video=video, imdb_id=data.get('imdb_id'),
                   imdb_url=data.get('imdb_url'), year=data.get('year'),
                   poster=data.get('poster'), plot=data.get('plot'),
                   plot_short=data.get('plot_simple'))
  new_info.save()


class VideoView(models.Model):
  """
  Simply a video view from a registered user
  """
  video = models.ForeignKey(Video)
  author = models.ForeignKey(User)
  
  created_date = models.DateTimeField(auto_now_add=True)
  # TODO:
  # In future we may want to store the ip address for geolocalisation and stats
  ip_address = models.GenericIPAddressField()
  
  def __unicode__(self):
    return '%s' % self.video.title


class VideoInfo(models.Model):
  """
  More information about the movie from IMDb
  """
  video = models.ForeignKey(Video)
  
  # information fields
  #actors
  #also_known_as = models.CharField(max_length=50, null=True, blank=True)
  #country = models.CharField(max_length=50, null=True, blank=True)
  poster = models.URLField(null=True, blank=True)
  plot = models.TextField(null=True, blank=True)
  plot_short = models.TextField(null=True, blank=True)
  
  imdb_id = models.CharField(max_length=50, null=True, blank=True)
  imdb_url = models.URLField()
  year = models.CharField(max_length=20, null=True, blank=True)
  
  
  created_date = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return 'info - %s' % self.video.title