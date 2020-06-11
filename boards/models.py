from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Boards(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Todos(models.Model):
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey(Boards, on_delete=models.CASCADE,blank=True,default=None,null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,default=None,null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "%s created at %s" % (str(self.title), str(self.created))
