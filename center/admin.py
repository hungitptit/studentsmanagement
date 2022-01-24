from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Test)
admin.site.register(Result)
# Register your models here.
