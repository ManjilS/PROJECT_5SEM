
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
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 

