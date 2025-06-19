from rest_framework import serializers
from .models import Document
from accounts.serializers import UserSerializer,DepartmentSerializer
from accounts.models import CustomUser, Department

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
    queryset=Department.objects.all(), source='department', write_only=True
     )
    uploaded_by_id = serializers.PrimaryKeyRelatedField(
    queryset=CustomUser.objects.all(), source='uploaded_by', write_only=True
       )
    file_url = serializers.SerializerMethodField()
    def get_file_url(self, obj):
      if obj.file:
            url = obj.file.url
            filename = obj.name or 'file'
            return url.replace('/upload/', f'/upload/fl_attachment:{filename}/')
      return None

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'description', 'category', 'file_url',
            'uploaded_by', 'department',
            'uploaded_by_id', 'department_id',
            'uploaded_at', 'updated_at',
        ]
        



