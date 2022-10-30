from django.contrib import admin
from .models import *

# Register your models here.


#admin.site.register(Student)
#admin.site.register(Kurator)
admin.site.register(Person)
admin.site.register(StudyGroup)
admin.site.register(Course)
admin.site.register(Subject)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = ['person', 'group', 'sex']

@admin.register(Kurator)
class KuratorAdmin(admin.ModelAdmin):
    fields = ['person']
