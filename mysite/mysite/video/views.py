# -*- coding: utf-8 -*-

#   Copyright (c) 2013, Thomas Gak Deluen. See
#   the COPYRIGHT file.

from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from videostream.models import VideoCategory, Video
from mysite.video.models import VideoView, VideoInfo, save_imdb_data_for_video

@login_required
@csrf_protect
def search(request):
  # TODO: the whole thing 
  return HttpResponse('Yes you made it here !</br>It\'s not finished yet ')

@login_required
@csrf_protect
@render_to('templates/video/upload.html')
def upload(request):
  page = 'upload'
  title = _('Upload')
  
  # TODO: Do upload stuff
  
  return locals()

@login_required
@csrf_protect
def new(request):
  video = request.raw_post_data  # get raw uploaded video
  old_name = request.GET.get('qqfile', 'video_name')
  #name = "%s.jpg" % utilities.keygen(30)
  #url = '%s/uploads/%s' % (settings.MEDIA_ROOT, name)
    
  #	Writing video {
  #destination = open(url, 'wb+')
  #destination.write(image)
  #destination.close()
  #	}

  return HttpResponse('Video received correctly with filename=%s' % old_name)
  

@login_required
@csrf_protect
@render_to('templates/video/genres.html')
def genres(request):
  page = 'genres'
  title = _('Genres')
  
  genres = VideoCategory.objects.all().order_by('title')
  
  return locals()


@login_required
@csrf_protect
@render_to('templates/video/genre.html')
def genre(request, slug):
  page = 'genre'
  genre = get_object_or_404(VideoCategory, slug=slug)
  title = _('%s' % genre.title)
  
  # just get videos whose slug equals `slug`
  movies = Video.objects.filter(Q(categories__slug__exact=slug))
  
  return locals()


@login_required
@csrf_protect
@render_to('templates/video/hot.html')
def hot(request, by='all'):
  page = 'hot'
  title = _('Hot')
  
  # get date descriptors
  today = datetime.today()
  year = today.year
  month = today.month
  day = today.day
  
  # Here we check whether the user wants the hottest videos
  # of all the time, of this year, of this month or just of today
  
  if by == 'month':
    # get videos with greater number of views by month
    hot = Video.objects.annotate(num_views=Count('videoview'))\
                       .filter(videoview__created_date__month=month)\
                       .order_by('-num_views')[:20]
  elif by == 'year':
    # get videos with greater number of views by year
    hot = Video.objects.annotate(num_views=Count('videoview'))\
                       .filter(videoview__created_date__year=year)\
                       .order_by('-num_views')[:20]
  elif by == 'day':
    # get videos with greater number of views by day
    hot = Video.objects.annotate(num_views=Count('videoview'))\
                       .filter(videoview__created_date__day=day)\
                       .order_by('-num_views')[:20]
  else:
    # get videos with greater number of views all time
    hot = Video.objects.annotate(num_views=Count('videoview'))\
                       .order_by('-num_views')[:20]
  
  
  return locals()
  

@login_required
@csrf_protect
@render_to('templates/video/watch.html')
def watch(request, video_id):
  page = 'watch'
  video = get_object_or_404(Video, id=video_id)
  title = _('Watch: %s' % video.title)
  
  # Little hack to repeat action to check if info exists
  i = 0
  while 1:
    try:
      info = VideoInfo.objects.get(video=video)
      break
    except VideoInfo.DoesNotExist:
      save_imdb_data_for_video(video)
    if i == 1:
      info = None
      break
    i += 1
  
  # must be changed accordingly
  VideoView(video=video, author=request.user, ip_address="127.0.0.1").save()
  
  return locals()
  