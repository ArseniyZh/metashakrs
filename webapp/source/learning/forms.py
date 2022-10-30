from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class AddSubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class AddCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class UpdateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class AddKuratorForm(ModelForm):
    class Meta:
        model = Kurator
        fields = '__all__'


class AddGroupForm(ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['number_group', 'course']


class AddEntrantForm(ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'sex']


class UpdateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'sex']