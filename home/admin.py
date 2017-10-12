from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User



class PInline(admin.StackedInline):
    model = Personnel
    can_delete = False
    verbose_name_plural = 'personnel'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
admin.site.register(Students_Courses)
admin.site.register(Instructors_Courses)
admin.site.register(Assignment)
admin.site.register(Courses)
admin.site.register(Department)
admin.site.register(Personnel)
admin.site.register(Roles)
admin.site.register(Attendance)
admin.site.register(Documents)
admin.site.register(Submissions)
admin.site.register(Events)
admin.site.register(Student_Period)

# Register your models here.
