"""MissingPeople URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static
from django.urls.conf import include
from center.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload', add_student, name = 'upload'),
    #path('success', success, name = 'success'),
    path('login/', login_form, name='login'),
    path('logout/', logout_func, name='logout'),
    path('signup/', signup, name='signup'),
    path('scoring', scoring, name='scoring'), 
    path('', get_classes, name='home'), 
    path('classes', get_classes, name='classes'),
    path('students', get_students, name='students') ,
    path('accounts/', include('allauth.urls')),
    path('studentdetail', show_student_detail, name='studentdetail'),
    path('editstudent', edit_student, name='editstudent'),
    path('settings', setting, name='settings'),
    path('manageClasses', manage_class, name='manage_class'),
    path('editclass', edit_class, name='editclass'),
    path('addclass', add_class, name = 'add_class'),
    path('deleteclass', delete_class, name = 'delete_class'),
    path('managesubject', manage_subject, name='manage_subject'),
    path('editsubject', edit_subject, name='editsubject'),
    path('addsubject', add_subject, name = 'add_subject'),
    path('deletesubject', delete_subject, name = 'delete_subject'),
    path('managetestt', manage_test, name='manage_test'),
    path('edittest', edit_test, name='editsubject'),
    path('addtest', add_test, name = 'add_test'),
    path('deletetest', delete_test, name = 'delete_test'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)