import pytest

from mihama import models


@pytest.fixture
def vulnerability():
    # versions: 3.2 to 5.2rc5
    return models.Vulnerability.parse_file("tests/fixtures/advisories/versions.json")


@pytest.mark.parametrize(
    "version,expected",
    [("3.1", False), ("3.2", True), ("5.2rc5", True), ("6.0", False)],
)
def test_is_affected_version_with_versions(
    vulnerability: models.Vulnerability, version: str, expected: bool
):
    assert vulnerability.is_affected_version(version) is expected
