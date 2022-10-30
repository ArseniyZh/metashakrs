from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


# Форма добавления учебной дисциплины
class AddSubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


# Форма добавления направления подготовки
class AddCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


# Форма обновления направления подготовки
class UpdateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


# Форма добавления куратора
class AddKuratorForm(ModelForm):
    class Meta:
        model = Kurator
        fields = '__all__'


# Форма добавления учебной группы
class AddGroupForm(ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['number_group', 'course']


# Форма добавления человека со статусом "абитуриент" в список студентов
class AddEntrantForm(ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'sex']


# Форма обновления студента
class UpdateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'sex']