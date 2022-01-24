from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Test)
admin.site.register(Result)
#admin.site.register(ExcelFile)
# Register your models here.
