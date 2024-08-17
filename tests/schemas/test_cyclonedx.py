import pytest

from mihama import schemas
from mihama.schemas.cyclonedx import Component


@pytest.fixture
def nested_component():
    # NOTE: it has 5 components in total (4 have purl, 1 does not have purl)
    with open("tests/fixtures/cyclonedx/nested_components.json") as f:
        return Component.model_validate_json(f.read())


def test_get_flatten_components(nested_component: Component):
    flatten = nested_component.get_flatten_components()
    assert len(flatten) == 5


@pytest.fixture
def bom(nested_component: Component):
    return schemas.CycloneDX(components=[nested_component])


def test_to_queries(bom: schemas.CycloneDX):
    # components do not have purl should be rejected
    # so the number should be 4
    assert len(bom.to_queries().queries) == 4
