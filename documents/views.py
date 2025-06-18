from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer
from accounts.permissions import IsAdmin, IsHR, IsEmployee, IsOwnerOrDepartmentHR


# Upload a new document (Employee, HR, or Admin)
class DocumentUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                uploaded_by=request.user,
                department=request.user.department
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            documents = Document.objects.filter(department=user.department, uploaded_by=user)
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


# Optional: Delete a document (only admin or owner)
class DocumentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrDepartmentHR]

    def delete(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        self.check_object_permissions(request, document)

        document.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
