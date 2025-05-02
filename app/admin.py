from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username','user_type']
admin.site.register(CustomUser,UserModel)
admin.site.register(course)
admin.site.register(session_year)
admin.site.register(student)
<<<<<<< HEAD
admin.site.register(Staff)

=======
admin.site.register(staff)
>>>>>>> 1dd7f445faf42a76f73e1b53b582e22e1141aa16
