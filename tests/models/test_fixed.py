import pytest

from mihama import models


@pytest.fixture
def vulnerability():
    # introduced: 0
    # fixed: 0.0.9
    return models.Vulnerability.parse_file("tests/fixtures/advisories/fixed.json")


@pytest.mark.parametrize(
    "package,version,expected",
    [
        (
            models.Package(ecosystem="Go", name="github.com/owncast/owncast"),
            "0.0.8",
            True,
        ),
        (
            models.Package(ecosystem="Go", name="github.com/owncast/owncast"),
            "0.0.9",
            False,
        ),
        (models.Package(ecosystem="Go", name="dummy"), "0.0.8", False),
    ],
)
def test_is_affected_package_version_with_fixed(
    vulnerability: models.Vulnerability,
    package: models.Package,
    version: str,
    expected: bool,
):
    assert (
        vulnerability.is_affected_package_version(version=version, package=package)
        is expected
    )
