from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Note(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='notes')

    def __str__(self):
        return self.title
