from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from school_management_system import views, Hod_Views, Student_Views, Staff_Views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.base,name='base'),
    
    #login path
    path('',views.login_view,name='login'),
    path('doLogin/',views.doLogin,name='doLogin'),
    path('doLogout/',views.doLogout,name='logout'),


    path('Hod/staff/Add',Hod_Views.add_staff,name='add_staff'),
    path('Hod/staff/View',Hod_Views.view_staff,name='view_staff'),


    #Student path
    path('student/home/',Student_Views.Student_home,name='student_home'),


   #Staff Path
   path('staff/home/',Staff_Views.Staff_home,name='staff_home'),
   path('staff/Notification/',Staff_Views.Staff_notification,name='staff_notification'),
   path('staff/mark_as_done/<str:status>',Staff_Views.Staff_mark_as_done,name='staff_mark_as_done'),
   path('staff/apply_leave/',Staff_Views.Staff_apply_leave,name='staff_apply_leave'),
    path('staff/apply_leave_save',Staff_Views.Staff_apply_leave_save,name='staff_apply_leave_save'),


    #profile update

    path('profile/',views.profile,name='profile'),
    path('profile/update',views.profile_update,name='profile_update'),
    #HOD panel
    path('Hod/home/',Hod_Views.home,name='home'),
    path('Hod/myprofile/',Hod_Views.myprofile,name='myprofile'),
    path('Hod/Student/add',Hod_Views.add_student,name='add_student'),
    path('Hod/Student/view',Hod_Views.VIEW_STUDENT,name='view_student'),
    path('Hod/Student/edit/<str:id>',Hod_Views.edit_student,name='edit_student'),
    path('Hod/Student/update',Hod_Views.update_student,name='update_student'),
    path('Hod/Student/delete/<str:admin>',Hod_Views.delete_student,name='delete_student'),
    

    path('Hod/Staff/add',Hod_Views.add_staff,name='add_staff'),
    path('Hod/Staff/view',Hod_Views.view_staff,name='view_staff'),
    path('Hod/Staff/edit/<str:id>',Hod_Views.edit_staff,name='edit_staff'),
    path('Hod/Staff/update',Hod_Views.update_staff,name='update_staff'),
    path('Hod/Staff/delete/<str:admin>',Hod_Views.delete_staff,name='delete_staff'),
    
    path('Hod/Course/add',Hod_Views.add_course,name='add_course'),
    path('Hod/Course/view',Hod_Views.view_course,name='view_course'),
    path('Hod/Course/edit/<str:id>',Hod_Views.edit_course,name='edit_course'),
    path('Hod/Course/update',Hod_Views.update_course,name='update_course'),
    path('Hod/Course/delete/<str:id>',Hod_Views.delete_course,name='delete_course'),
    


    path('Hod/Subject/add',Hod_Views.add_subject,name='add_subject'),
    path('Hod/Subject/view',Hod_Views.view_subject,name='view_subject'),
    path('Hod/Subject/edit/<str:id>',Hod_Views.edit_subject,name='edit_subject'),
    path('Hod/Subject/update',Hod_Views.update_subject,name='update_subject'),
    path('Hod/Subject/delete/<str:id>',Hod_Views.delete_subject,name='delete_subject'),

    path('Hod/Session/add',Hod_Views.add_session,name='add_session'),
    path('Hod/Session/view',Hod_Views.view_session,name='view_session'),
    path('Hod/Session/edit/<str:id>',Hod_Views.edit_session,name='edit_session'),
    path('Hod/Session/update',Hod_Views.update_session,name='update_session'),
    path('Hod/Session/delete/<str:id>',Hod_Views.delete_session,name='delete_session'),
    
    path('Hod/Staff/send_notification',Hod_Views.send_staff_notification,name='send_staff_notification'),
    path('Hod/Staff/save_notification',Hod_Views.save_staff_notification,name='save_staff_notification'),

    path('Hod/Staff/leave_view',Hod_Views.view_staff_leave,name='view_staff_leave'),
    path('Hod/Staff/approve_leave/<str:id>',Hod_Views.staff_approve_leave,name='staff_approve_leave'),
    path('Hod/Staff/disapprove_leave/<str:id>',Hod_Views.staff_disapprove_leave,name='staff_disapprove_leave'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
