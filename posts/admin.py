from django.contrib import admin
from posts.models import Comment, Notification, Post, Vote
# Register your models here.
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Notification),
