from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer
from accounts.permissions import IsAdmin, IsHR, IsEmployee, IsOwnerOrDepartmentHR
from rest_framework.parsers import MultiPartParser, FormParser
import logging
logger = logging.getLogger(__name__)

class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data  

        try:
            # Prepare mutable data dictionary for serializer
            serializer_data = {
                'name': data.get('name'),
                'description': data.get('description'),
                'category': data.get('category'),
                'uploaded_by_id': user.id,
                'file': data.get('file'),
            }

            # Set department ID
            if user.role != 'ADMIN':
                if not hasattr(user, 'department') or not user.department:
                    return Response(
                        {"error": "Non-admin users must have a department assigned."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                serializer_data['department_id'] = user.department.id
            else:
                if 'department' not in data:
                    return Response(
                        {"error": "Department is required for admin uploads."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                serializer_data['department_id'] = int(data.get('department'))

            # Validate and save
            serializer = DocumentSerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error during document upload: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# List documents available to the user based on role
class DocumentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_admin():
            documents = Document.objects.all()
        elif user.is_hr():
            documents = Document.objects.filter(department=user.department)
        elif user.is_employee():
            documents = Document.objects.filter(department=user.department)
        else:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieve a document for download (with object-level permission check)
class DocumentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrDepartmentHR]

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        self.check_object_permissions(request, document)

        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DocumentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        try:
            document_ids = request.data.get('ids', [])
            
            if not document_ids:
                return Response(
                    {"error": "No document IDs provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Verify the user has permission to delete these documents
            documents = Document.objects.filter(
                id__in=document_ids,
                uploaded_by=request.user  # Only allow deleting own documents
            )
        
            count, _ = documents.delete()
            
            return Response(
                {"message": f"Successfully deleted {count} documents"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class TotalDocumentsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        total_documents = Document.objects.count()
        return Response({"total": total_documents})       