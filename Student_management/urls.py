"""Student_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from student_management_app import views,hodviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', views.showDemoPage),
    path('', views.showLoginPage),
    path('get_user_details/', views.GetUserDetails),
    path('logout_user/', views.logout_user,name='logout'),
    path('doLogin/', views.doLogin),
    path('admin_home/', hodviews.admin_home, name="admin_home"),
    path('add_staff/', hodviews.add_staff),
    path('add_staff_save/', hodviews.add_staff_save),
    path('add_course/', hodviews.add_course),
    path('add_course_save/', hodviews.add_course_save),
    path('add_student/', hodviews.add_student),
    path('add_student_save/', hodviews.add_student_save),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
