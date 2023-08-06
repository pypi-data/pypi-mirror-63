from django.db import models

from huscy.projects.models import Project


class DocumentType(models.Model):
    name = models.CharField(max_length=64)


class Document(models.Model):
    def get_upload_path(self, filename):
        return f'documents/{filename}'

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)

    filehandle = models.FileField(upload_to=get_upload_path)
    filename = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    uploaded_by = models.CharField(max_length=128, editable=False)
