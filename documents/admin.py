from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','description','uploaded_at', 'updated_at', 'uploaded_by')
    search_fields = ('name', 'uploaded_by__username')
    list_filter = ('uploaded_at', 'updated_at', 'uploaded_by')
# Register your models here.
