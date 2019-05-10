from django.contrib import admin
from blog.models import Entry, UserProfile, Comment

admin.site.register(Entry)
admin.site.register(UserProfile)
admin.site.register(Comment)