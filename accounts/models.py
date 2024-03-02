from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    about_user = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.username