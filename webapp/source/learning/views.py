from django.shortcuts import render
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import tasks




def index(request):
    return render(request, 'index.html')


# Список учебных дисциплин
def subject_list(request):
    form = AddSubjectForm()
    subjects = Subject.objects.all()  # Получение всех учебных дисциплин
    context = {
        'subjects': subjects,
        'form': form
    }

    return render(request, 'learning/subject_list.html', context)


# Создание учебной дисциплины
class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name']


# Обновление учебной дисциплины
class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name']


# Удаление учебной дисциплины
class SubjectDeleteView(DeleteView):
    model = Subject
    success_url = reverse_lazy('index')


# Список направления подготовки
def courses(request):
    form = AddCourseForm()
    courses = Course.objects.all()  # Получение всех направлений подготовки
    context = {
        'courses': courses,
        'form': form
    }

    return render(request, 'learning/course_list.html', context)


# Создание направления подготовки
class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'subjects', 'kurator']


# Обновление направления подготовки
class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'subjects', 'kurator']


# Удаление направления подготовки
class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('index')


# Список кураторов
def kurators_list(request):
    if request.method == 'POST':
        form = AddKuratorForm(request.POST)
        if form.is_valid():
            person = Person.objects.get(id=request.POST.get('person'))  # Получаем определенного человека
            person.status = '2'  # Устанавливаем ему статус "куратор"
            person.save()
            kurator = Kurator()
            kurator.person = person  # Связываем модель куратора с человеком
            kurator.save()
    else:
        form = AddKuratorForm()
    kurators = Kurator.objects.all()  # Получение всех кураторов

    context = {
        'kurators': kurators,
        'form': form
    }

    return render(request, 'learning/kurator_list.html', context)


# Удаление куратора
class KuratorDeleteView(DeleteView):
    model = Kurator
    success_url = reverse_lazy('index')


# Список учебных групп
def study_group_list(request):
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            group = StudyGroup()
            course = Course(id=request.POST.get('course'))  # Получаем модель определенного учебного направления
            group.number_group = request.POST.get('number_group')  # Устанавливаем номер группы
            group.course = course  # Связываем учебную группу с курсом
            group.save()
    else:
        form = AddGroupForm()
    groups = StudyGroup.objects.all()

    context = {
        'groups': groups,
        'form': form
    }

    return render(request, 'learning/study_group_list.html', context)


# Детали учебной группы
def study_group_detail(request, id):
    group = StudyGroup.objects.get(id=id)  # Получение учебной группы
    students = Student.objects.all().filter(group=group)  # Получение студентов этой группы

    context = {
        'group': group,
        'students': students
    }

    return render(request, 'learning/study_group_detail.html', context)


# Удаление учебной группы
class StudyGroupDeleteView(DeleteView):
    model = StudyGroup
    success_url = reverse_lazy('index')


# Список студентов и абитуриентов
def student_list(request):
    entrants = Person.objects.all().filter(status__exact='3')  # Получение людей со статусом "абитуриент"
    students = Student.objects.all()  # Получение всех студентов

    context = {
        'entrants': entrants,
        'students': students,
    }

    return render(request, 'learning/student_list.html', context)


# Детали абитуриента
def entrant_detail(request, id):
    entrant = Person.objects.get(id=id)
    form = AddEntrantForm()

    context = {
        'entrant': entrant,
        'form': form
    }
    return render(request, 'learning/entrant_detail.html', context)


# Добавление абитуриента в список студентов
def student_add(request, id):
    if request.method == 'POST':
        form = AddEntrantForm(request.POST)
        if form.is_valid():
            entrant = Person.objects.get(id=id)  # Получаем определенного человека
            entrant.status = '1'  # Устанавливаем ему статус "студент"
            entrant.save()

            group = StudyGroup.objects.get(id=request.POST.get('group'))  # Получаем модель определенной группы
            students_group = Student.objects.all().filter(group=group)  # Получаем всех студентов этой группы
            if students_group.count() <= 20:  # Проверяем наличие свободных мест
                student = Student()
                student.person = entrant  # Заносим абитурента в список студентов
                student.group = group  # Устанавливаем ему группу
                student.sex = request.POST.get('sex')  # Устанавливаем ему пол
                student.save()
            else:
                return HttpResponse('<h1>В группе максимальное количество студентов</h1>')

    entrants = Person.objects.all().filter(status__exact='3')  # Получаем всех людей со статусом "абитуриент"
    students = Student.objects.all().order_by('group')  # Получаем всех студентов, которые отсортированы по группам

    context = {
        'entrants': entrants,
        'students': students,
    }
    return render(request, 'learning/student_list.html', context)


# Детали студента
def student_detail(request, id):
    student = Student.objects.get(id=id)  # Получаем определенного студента
    if request.method == 'POST':
        form = UpdateStudentForm(request.POST)
        if form.is_valid():
            student.group = StudyGroup.objects.get(id=request.POST.get('group'))  # Устанавливаем группу студенту
            student.sex = request.POST.get('sex')  # Устанавливаем пол студенту
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


# Удаление студента и установка человеку статуса "абитуриент"
def student_delete(request, id):
    student = Student.objects.get(id=id)  # Получаем определенного студента
    person = student.person  # Узнаем человека
    person.status = '3'  # Устанавливаем человеку статус "абитуриент"
    student.delete()  # Удаляем модель определенного студента
    person.save()
    return HttpResponseRedirect('/')


# Отчет (котики лучше)
def report(request):
    courses = Course.objects.all()  # Получение всех учебных направлений
    groups = StudyGroup.objects.all()  # Получение всех учебных групп
    students = Student.objects.all()  # Получение всех студентов

    context = {
        'courses': courses,
        'groups': groups,
        'students': students
    }
    return render(request, 'learning/report.html', context)


# Ассинхронное выполнение задачи с помощью Celery и Redis
def report_create(request):
    tasks.report.delay()
    return HttpResponseRedirect('/')