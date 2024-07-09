from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  username = None
  email = models.EmailField(unique = True)
  phone_number = models.CharField(max_length=10, unique=True)
  user_bio = models.CharField(max_length=100)
  user_profile_image = models.ImageField(upload_to="profile")
  USERNAME_FIELD = 'phone_number'
  REQUIRED_FIELDS = []