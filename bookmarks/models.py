from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    link = models.CharField(max_length=150)
    link_text = models.CharField(max_length=255)
    byline = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.link_text +  ' in ' + self.folder.name