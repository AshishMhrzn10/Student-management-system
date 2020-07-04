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
from student_management_app import views,hodviews,studentviews,staffviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', views.showDemoPage),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.showLoginPage, name="show_login"),
    path('get_user_details/', views.GetUserDetails),
    path('logout_user/', views.logout_user,name='logout'),
    path('doLogin/', views.doLogin, name="do_login"),
    path('admin_home/', hodviews.admin_home, name="admin_home"),
    path('add_staff/', hodviews.add_staff, name="add_staff"),
    path('add_staff_save/', hodviews.add_staff_save, name="add_staff_save"),
    path('add_course/', hodviews.add_course, name="add_course"),
    path('add_course_save/', hodviews.add_course_save, name="add_course_save"),
    path('add_student/', hodviews.add_student, name="add_student"),
    path('add_student_save/', hodviews.add_student_save, name="add_student_save"),
    path('add_subject/', hodviews.add_subject, name="add_subject"),
    path('add_subject_save/', hodviews.add_subject_save, name="add_subject_save"),
    path('manage_staff/', hodviews.manage_staff, name="manage_staff"),
    path('manage_student/', hodviews.manage_student, name="manage_student"),
    path('manage_course/', hodviews.manage_course, name="manage_course"),
    path('manage_subject/', hodviews.manage_subject, name="manage_subject"),
    path('edit_staff/<str:staff_id>', hodviews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', hodviews.edit_staff_save, name="edit_staff_save"),
    path('edit_student/<str:student_id>', hodviews.edit_student, name="edit_student"),
    path('edit_student_save/', hodviews.edit_student_save, name="edit_student_save"),
    path('edit_subject/<str:subject_id>', hodviews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', hodviews.edit_subject_save, name="edit_subject_save"),
    path('edit_course/<str:course_id>', hodviews.edit_course, name="edit_course"),
    path('edit_course_save/', hodviews.edit_course_save, name="edit_course_save"),
    path('view_attendance/', hodviews.view_attendance, name="view_attendance"),
    path('student_feedback/', hodviews.student_feedback, name="student_feedback"),
    path('staff_feedback/', hodviews.staff_feedback, name="staff_feedback"),
    path('student_leave/', hodviews.student_leave, name="student_leave"),
    path('staff_leave/', hodviews.staff_leave, name="staff_leave"),
    path('manage_session/', hodviews.manage_session, name="manage_session"),
    path('add_session_save/', hodviews.add_session_save, name="add_session_save"),

    #Staff url path
    path('staff_home/', staffviews.staff_home, name="staff_home"),
    path('staff_take_attendance/', staffviews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance/', staffviews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students/', staffviews.get_students, name="get_students"),
    path('get_attendance_dates/', staffviews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', staffviews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data/', staffviews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data/', staffviews.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave/', staffviews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', staffviews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedbacks/', staffviews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', staffviews.staff_feedback_save, name="staff_feedback_save"),

    #Student url path
    path('student_home/', studentviews.student_home, name="student_home"),
    path('student_view_attendance/', studentviews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', studentviews.student_view_attendance_post, name="student_view_attendance_post"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
