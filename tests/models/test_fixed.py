import pytest

from mihama import models


@pytest.fixture
def vulnerability():
    # introduced: 0
    # fixed: 0.0.9
    return models.Vulnerability.parse_file("tests/fixtures/advisories/fixed.json")


@pytest.mark.parametrize(
    "version,expected", [("0.0.8", True), ("0.0.9", False), ("1.0.0", False)]
)
def test_is_affected_version_with_fixed(
    vulnerability: models.Vulnerability, version: str, expected: bool
):
    assert vulnerability.is_affected_version(version) is expected
