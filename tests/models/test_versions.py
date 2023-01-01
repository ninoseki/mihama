import pytest

from mihama import models


@pytest.fixture
def vulnerability():
    # versions: 3.2 to 5.2rc5
    return models.Vulnerability.parse_file("tests/fixtures/advisories/versions.json")


@pytest.mark.parametrize(
    "package,version,expected",
    [
        (models.Package(ecosystem="PyPI", name="plone"), "3.1", False),
        (models.Package(ecosystem="PyPI", name="plone"), "3.2", True),
        (models.Package(ecosystem="PyPI", name="plone"), "5.2rc5", True),
        (models.Package(ecosystem="PyPI", name="plone"), "6.0", False),
        (models.Package(ecosystem="PyPI", name="dummy"), "3.2", False),
        (models.Package(ecosystem="PyPI", name="dummy"), "5.2rc5", False),
    ],
)
def test_is_affected_package_version_with_versions(
    vulnerability: models.Vulnerability,
    package: models.Package,
    version: str,
    expected: bool,
):
    assert (
        vulnerability.is_affected_package_version(version=version, package=package)
        is expected
    )
