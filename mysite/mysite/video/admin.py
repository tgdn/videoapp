# -*- coding: utf-8 -*-

from django.contrib import admin
from mysite.video.models import VideoView, VideoInfo

admin.site.register(VideoView)
admin.site.register(VideoInfo)