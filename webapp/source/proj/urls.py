"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from learning import views as lv
from users import views as uv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lv.index, name='index'),

    path('subject_list/', lv.subject_list, name='subject_list'),
    path('subject/new', lv.SubjectCreateView.as_view(), name='subject_new'),
    path('subject/<str:pk>/edit', lv.SubjectUpdateView.as_view(), name='subject_edit'),
    path('subject/<str:pk>/delete', lv.SubjectDeleteView.as_view(), name='subject_delete'),

    path('course_list/', lv.courses, name='course_list'),
    path('course/new/', lv.CourseCreateView.as_view(), name='course_new'),
    path('course/<str:pk>/edit', lv.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<str:pk>/delete', lv.CourseDeleteView.as_view(), name='course_delete'),

    path('kurator_list/', lv.kurators_list, name='kurator_list'),
    path('kurator/<str:pk>/delete', lv.KuratorDeleteView.as_view(), name='kurator_delete'),

    path('study_group_list/', lv.study_group_list, name='study_group_list'),
    path('study_group/<str:id>/detail', lv.study_group_detail, name='study_group_detail'),
    path('study_group/<str:pk>/delete', lv.StudyGroupDeleteView.as_view(), name='study_group_delete'),

    path('student_list/', lv.student_list, name='student_list'),
    path('entrant/<str:id>/detail', lv.entrant_detail, name='entrant_detail'),
    path('student/<str:id>/add', lv.student_add, name='student_add'),
    path('student/<str:id>/detail', lv.student_detail, name='student_detail'),
    path('student/<str:id>/delete', lv.student_delete, name='student_delete'),

    path('sign_up/', uv.sign_up, name='sign_up'),
    path('logout/', uv.user_logout, name='logout'),
    path('login/', uv.user_login, name='login'),

    path('report/', lv.report, name='report'),
    path('report/create', lv.report_create, name='report_create'),
]
