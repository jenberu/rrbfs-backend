from django.contrib import admin
from .models import CustomUser, Department
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'department')
    search_fields = ('username', 'email')
    list_filter = ('role', 'department')
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register your models here.
