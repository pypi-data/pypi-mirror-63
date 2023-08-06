from itertools import cycle

import pytest
from model_bakery import baker

from huscy.project_documents.services import get_documents


@pytest.fixture
def documents():
    projects = baker.make('projects.Project', _quantity=3)
    return baker.make('project_documents.Document', project=cycle(projects), _quantity=6)


@pytest.mark.django_db
def test_get_documents(documents):
    result = get_documents()

    assert list(result) == documents


@pytest.mark.django_db
def test_get_documents_filtered_by_project(documents):
    result = get_documents(documents[0].project)

    assert len(result) == 2
    assert list(result) == [documents[0], documents[3]]
