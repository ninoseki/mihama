import pytest

from mihama import models


@pytest.fixture
def vulnerability():
    # the vulnerability has multiple packages in affected
    return models.Vulnerability.parse_file(
        "tests/fixtures/advisories/multi_packages_fixed.json"
    )


@pytest.fixture
def plone_package():
    return models.Package(ecosystem="PyPI", name="Plone")


@pytest.mark.parametrize(
    "package,version,expected",
    [
        (models.Package(ecosystem="PyPI", name="Plone"), "5.2.2", True),
        (models.Package(ecosystem="PyPI", name="Plone"), "5.2.3", False),
        (models.Package(ecosystem="PyPI", name="plone.app.event"), "3.2.9", True),
        (models.Package(ecosystem="PyPI", name="plone.app.event"), "3.2.10", False),
    ],
)
def test_is_affected_package_version_with_multiple_package(
    vulnerability: models.Vulnerability,
    package: models.Package,
    version: str,
    expected: bool,
):
    assert (
        vulnerability.is_affected_package_version(version=version, package=package)
        is expected
    )
