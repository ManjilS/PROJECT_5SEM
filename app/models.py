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

class course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=10)
    course_created_date = models.DateField(auto_now_add=True)
    course_updated_date = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.course_name
    
class session_year(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    

    def __str__(self):
        return str(self.session_start_year) + " - " + str(self.session_end_year)
    

class staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    phone_number = models.TextField()
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.admin.first_name) + " " + str(self.admin.last_name)

class student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, default='')
    course_id = models.ForeignKey(course, on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(session_year, on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return str(self.admin.first_name) + " " + str(self.admin.last_name)
