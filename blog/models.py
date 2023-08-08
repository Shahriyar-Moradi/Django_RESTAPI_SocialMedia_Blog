# from django.utils.timezone import timezone

from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    # title=models
    text = models.TextField()
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.room_number)
        return f"{self.text} by {self.post_author}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.text


class PostLiked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"like for {self.post}"
