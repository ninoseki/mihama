import pytest

from mihama import schemas


@pytest.fixture
def spdx():
    # this file contains one PURL package only
    with open("tests/fixtures/spdx/example.json") as f:
        return schemas.SPDX.model_validate_json(f.read())


def test_to_queries(spdx: schemas.SPDX):
    assert len(spdx.to_queries().queries) == 1
