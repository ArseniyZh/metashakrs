from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid


# Create your models here.

# Модель расширяет модель User
class Person(models.Model):
    VOTE_TYPE = (
        ('1', 'Студент'),
        ('2', 'Куратор'),
        ('3', 'Абитуриент'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30,
                                  help_text='Введите имя',
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=30,
                                 help_text='Введите фамилию',
                                 verbose_name='Фамилия')
    status = models.CharField(max_length=20, choices=VOTE_TYPE, default=3)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_students(self) -> list:
        # Получение людей со статусом "студент"
        return [student for student in self.user.person.all().filter(status='1')]


# Модель студента
class Student(models.Model):
    SEX_VOTE = (
        ('1', 'Мужской'),
        ('2', 'Женский'),
    )
    person = models.ForeignKey('Person', null=True, blank=True, on_delete=models.DO_NOTHING)
    group = models.ForeignKey('StudyGroup', null=True, blank=True, on_delete=models.CASCADE)
    sex = models.CharField(max_length=20, choices=SEX_VOTE)

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name}'


# Модель куратора
class Kurator(models.Model):
    person = models.ForeignKey('Person', null=True, blank=True, unique=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name}'


# Модель учебной группы
class StudyGroup(models.Model):
    number_group = models.IntegerField(unique=True,
                                       help_text='Введите номер группы',
                                       verbose_name='Номер группы')
    course = models.ForeignKey('Course', null=True, blank=True, on_delete=models.DO_NOTHING)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.number_group)

    def get_students(self) -> list:
        # Получение списка студентов определенной группы
        return [student for student in Student.objects.all().filter(group=self.id)]

    def male_female(self) -> str:
        # Получение строки с информацией о количестве мальчиков\девочек
        students = Student.objects.all().filter(group=self.id)  # Берем всех студентов определенной группы
        # Получаем количество мальчиков\девочек
        male = students.filter(sex='1').count()
        female = students.filter(sex='2').count()
        return f'мальчиков: {male} девочек: {female}'

    def free_space(self) -> int:
        # Получение количества свободных мест
        return 20 - Student.objects.all().filter(group=self.id).count()


# Модель направления подготовки
class Course(models.Model):
    name = models.CharField(max_length=50,
                            help_text='Введите название направления подготовки',
                            verbose_name='Направление подготовки')
    subjects = models.ManyToManyField('Subject')
    kurator = models.OneToOneField('Kurator', on_delete=models.DO_NOTHING)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    def get_subjects(self) -> list:
        # Получение учебных дисциплин направления подготовки
        return [subject for subject in self.subjects.all()]

    def get_absolute_url(self):
        return reverse('index')


# Модель учебного направления
class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            help_text='Введите название учебной дисциплины',
                            verbose_name='Учебная дисциплина')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')
