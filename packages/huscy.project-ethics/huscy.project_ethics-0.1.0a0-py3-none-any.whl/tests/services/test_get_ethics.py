from itertools import cycle

import pytest
from model_bakery import baker

from huscy.project_ethics.services import get_ethics

pytestmark = pytest.mark.django_db


def test_get_ethics():
    ethics = create_ethics()

    result = get_ethics()

    assert list(result) == ethics


def test_get_ethics_filtered_by_project():
    ethics = create_ethics()

    result = get_ethics(ethics[0].project)

    assert len(result) == 2
    assert list(result) == [ethics[0], ethics[3]]


def create_ethics():
    projects = baker.make('projects.Project', _quantity=3)
    return baker.make('project_ethics.Ethic', project=cycle(projects), _quantity=6)
