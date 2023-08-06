from huscy.project_documents.filters import DocumentFilter
from huscy.project_documents.models import Document, DocumentType


def create_document(project, filehandle, document_type, creator):
    filename = filehandle.name.split('/')[-1]

    return Document.objects.create(
        project=project,
        document_type=document_type,
        filehandle=filehandle,
        filename=filename,
        uploaded_by=creator.get_full_name(),
    )


def get_document_types():
    return DocumentType.objects.order_by('name')


def get_documents(project=None):
    queryset = Document.objects.order_by('uploaded_at')
    filters = dict(project=project and project.pk)
    return DocumentFilter(filters, queryset).qs
