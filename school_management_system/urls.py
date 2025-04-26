
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views,Hod_Views,Student_Views,Staff_Views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.base,name='base'),
    
    #login path
    path('',views.login_view,name='login'),
    path('doLogin/',views.doLogin,name='doLogin'),
    path('doLogout/',views.doLogout,name='logout'),

   
    

    #profile update

    path('profile/',views.profile,name='profile'),
    path('profile/update',views.profile_update,name='profile_update'),
    #HOD panel
    path('Hod/home/',Hod_Views.home,name='home'),
    path('Hod/myprofile/',Hod_Views.myprofile,name='myprofile'),
    path('Hod/Student/add',Hod_Views.add_student,name='add_student'),
    path('Hod/Student/view',Hod_Views.VIEW_STUDENT,name='view_student'),
    path('Hod/Student/edit/<int:admin_id>/', Hod_Views.edit_student, name='edit_student'),
    path('Hod/Student/delete/<int:admin_id>/', Hod_Views.delete_student, name='delete_student'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 

