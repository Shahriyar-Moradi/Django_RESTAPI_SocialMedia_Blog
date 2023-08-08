from django.contrib import admin

# Register your models here.
from .models import Post,PostLiked,Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(PostLiked)
admin.site.register(Comment)