import pytest

from mihama import models


@pytest.fixture
def vulnerability():
    # introduced: 0
    # last_affected: 4.1.0
    return models.Vulnerability.parse_file(
        "tests/fixtures/advisories/last_affected.json"
    )


@pytest.mark.parametrize(
    "version,expected", [("1.0.0", True), ("4.1.0", True), ("4.1.1", False)]
)
def test_is_affected_version_with_last_affected(
    vulnerability: models.Vulnerability,
    version: str,
    expected: bool,
):
    assert vulnerability.is_affected_version(version) is expected
