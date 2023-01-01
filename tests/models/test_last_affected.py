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
    "package,version,expected",
    [
        (models.Package(ecosystem="PyPI", name="opencv-python"), "4.1.0", True),
        (models.Package(ecosystem="PyPI", name="opencv-python"), "4.1.1", False),
        (models.Package(ecosystem="PyPI", name="dummy"), "4.1.0", False),
    ],
)
def test_is_affected_package_version_with_last_affected(
    vulnerability: models.Vulnerability,
    package: models.Package,
    version: str,
    expected: bool,
):
    assert (
        vulnerability.is_affected_package_version(version=version, package=package)
        is expected
    )
