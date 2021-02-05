from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class user(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class information(models.Model):

    designation = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class link(models.Model):

    SNo = models.IntegerField(default=0)
    link = models.URLField()




