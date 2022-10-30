from django.shortcuts import render
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import tasks
import os
from django.conf import settings

# Create your views here.


def index(request):
    return render(request, 'index.html')


class SubjectListView(ListView):
    model = Subject

def subject_list(request):
    form = AddSubjectForm()
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'form': form
    }

    return render(request, 'learning/subject_list.html', context)


class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name']


class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name']


class SubjectDeleteView(DeleteView):
    model = Subject
    success_url = reverse_lazy('index')


def courses(request):
    form = AddCourseForm()
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'form': form
    }

    return render(request, 'learning/course_list.html', context)


class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'subjects', 'kurator']


class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'subjects', 'kurator']


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('index')


def kurators_list(request):
    if request.method == 'POST':
        form = AddKuratorForm(request.POST)
        if form.is_valid():
            person = Person.objects.get(id=request.POST.get('person'))
            person.status = '2'
            person.save()
            kurator = Kurator()
            kurator.person = person
            kurator.person.status = 'Куратор'
            kurator.save()
    else:
        form = AddKuratorForm()
    kurators = Kurator.objects.all()

    context = {
        'kurators': kurators,
        'form': form
    }

    return render(request, 'learning/kurator_list.html', context)


def delete_kurator(request, id):
    Kurator.objects.get(id=id).delete()
    return HttpResponseRedirect('/')

class KuratorDeleteView(DeleteView):
    model = Kurator
    success_url = reverse_lazy('index')


def study_group_list(request):
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            group = StudyGroup()
            course = Course(id=request.POST.get('course'))
            group.number_group = request.POST.get('number_group')
            group.course = course
            group.save()
    else:
        form = AddGroupForm()
    groups = StudyGroup.objects.all()

    context = {
        'groups': groups,
        'form': form
    }

    return render(request, 'learning/study_group_list.html', context)


def study_group_detail(request, id):
    group = StudyGroup.objects.get(id=id)
    students = Student.objects.all().filter(group=group)

    context = {
        'group': group,
        'students': students
    }

    return render(request, 'learning/study_group_detail.html', context)


class StudyGroupDeleteView(DeleteView):
    model = StudyGroup
    success_url = reverse_lazy('index')


def student_list(request):
    entrants = Person.objects.all().filter(status__exact='3')
    students = Student.objects.all()

    context = {
        'entrants': entrants,
        'students': students,
    }

    return render(request, 'learning/student_list.html', context)


def entrant_detail(request, id):
    entrant = Person.objects.get(id=id)
    form = AddEntrantForm()

    context = {
        'entrant': entrant,
        'form': form
    }
    return render(request, 'learning/entrant_detail.html', context)


def student_add(request, id):
    if request.method == 'POST':
        form = AddEntrantForm(request.POST)
        if form.is_valid():
            entrant = Person.objects.get(id=id)
            entrant.status = '1'
            entrant.save()

            group = StudyGroup.objects.get(id=request.POST.get('group'))
            students_group = Student.objects.all().filter(group=group)
            if students_group.count() <= 20:
                student = Student()
                student.person = entrant
                student.group = group
                student.sex = request.POST.get('sex')
                student.save()
            else:
                return HttpResponse('<h1>В группе максимальное количество студентов</h1>')

    entrants = Person.objects.all().filter(status__exact='3')
    students = Student.objects.all().order_by('group')

    context = {
        'entrants': entrants,
        'students': students,
    }
    return render(request, 'learning/student_list.html', context)


def student_detail(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateStudentForm(request.POST)
        if form.is_valid():
            student.group = StudyGroup.objects.get(id=request.POST.get('group'))
            student.sex = request.POST.get('sex')
            student.save()
            return HttpResponseRedirect('/')
    else:
        form = UpdateStudentForm()

    sex = 'Мужской' if student.sex == '1' else 'Женский'

    context = {
        'student': student,
        'sex': sex,
        'form': form
    }

    return render(request, 'learning/student_detail.html', context)


def student_delete(request, id):
    student = Student.objects.get(id=id)
    person = student.person
    person.status = '3'
    student.delete()
    person.save()
    return HttpResponseRedirect('/')


def report(request):
    courses = Course.objects.all()
    groups = StudyGroup.objects.all()
    students = Student.objects.all()

    context = {
        'courses': courses,
        'groups': groups,
        'students': students
    }
    return render(request, 'learning/report.html', context)


def report_create(request):
    tasks.report.delay()
    return HttpResponseRedirect('/')