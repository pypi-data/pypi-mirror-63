from django_filters import rest_framework as filters

from huscy.project_documents import models


class DocumentFilter(filters.FilterSet):
    class Meta:
        model = models.Document
        fields = (
            'project',
        )
