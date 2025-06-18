from django.db import models
from accounts.models import CustomUser, Department

def upload_path(instance, filename):
    return f"{instance.department.name}/{filename}"

class Document(models.Model):
    CATEGORY_CHOICES = [
    ('policy', 'Policy'),
    ('payroll', 'Payroll'),
    ('leave', 'Leave Documents'),
    ('report', 'Reports'),
    ('project', 'Project Files'),
    ('training', 'Training'),
    ('announcement', 'Announcements'),
    ('template', 'Templates'),
    ('hr', 'HR Documents'),
    ('legal', 'Legal'),
    ('other', 'Other'),
     ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='report')
    file = models.FileField(upload_to=upload_path)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
