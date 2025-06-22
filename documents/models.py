from django.db import models
from accounts.models import CustomUser, Department
from cloudinary_storage.storage import MediaCloudinaryStorage

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
    file = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage()  
    )    
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.name
