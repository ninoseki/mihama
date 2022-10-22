import pytest

from app import schemas
from app.schemas.cyclonedx import Component


@pytest.fixture
def nested_component():
    # NOTE: it has 5 components in total (4 have purl, 1 does not have purl)
    return Component.parse_file("tests/fixtures/cyclonedx/nested_components.json")


def test_get_flatten_components(nested_component: Component):
    flatten = nested_component.get_flatten_components()
    assert len(flatten) == 5


@pytest.fixture
def bom(nested_component: list[Component]):
    return schemas.CycloneDX(components=[nested_component])


def test_to_batch_query(bom: schemas.CycloneDX):
    batch_query = bom.to_batch_query()
    # components do not have purl should be rejected
    # so the number should be 4
    assert len(batch_query.queries) == 4
