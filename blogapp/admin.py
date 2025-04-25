from django.contrib import admin
from .models import Blog, Comment
from django.db import models

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)


#
