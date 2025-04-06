from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
   USER= (
      (1,'hod'),
      (2,'staff'),
      (3,'student'),
    )
   user_type=models.CharField(choices=USER,max_length=50,default=1)
   profile_pic = models.ImageField(upload_to='media/profile_pics')

# Create your models here.
