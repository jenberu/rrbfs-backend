from django.urls import path
from .views import (DocumentUploadView, 
                    DocumentListView,
                     DocumentDetailView, 
                     DocumentDeleteView,
                     TotalDocumentsView)

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='upload-document'),
    path('', DocumentListView.as_view(), name='list-documents'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('delete/', DocumentDeleteView.as_view(), name='document-delete'),
    path("total-documents/", TotalDocumentsView.as_view(), name="total-documents"),

]
