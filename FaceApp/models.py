from django.db import models

from django.contrib.auth.models import User


class Gallary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    image = models.ImageField(default='Image.jpg', upload_to="profile_pics")

    def __str__(self):
        return self.title
