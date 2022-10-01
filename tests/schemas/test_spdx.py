import pytest

from app import schemas


@pytest.fixture
def spdx():
    # this file contains one PURL package only
    return schemas.SPDX.parse_file("tests/fixtures/spdx/example.json")


def test_to_batch_query(spdx: schemas.SPDX):
    batch_query = spdx.to_batch_query()
    assert len(batch_query.queries) == 1
