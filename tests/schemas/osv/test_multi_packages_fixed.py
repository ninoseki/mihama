import pytest

from mihama import schemas


@pytest.fixture
def vuln():
    # the vulnerability has multiple packages in affected
    with open("tests/fixtures/advisories/multi_packages_fixed.json") as f:
        return schemas.Vulnerability.model_validate_json(f.read())


@pytest.fixture
def plone_package():
    return schemas.Package(ecosystem="PyPI", name="Plone")


@pytest.mark.parametrize(
    ("package", "version", "expected"),
    [
        (schemas.Package(ecosystem="PyPI", name="Plone"), "5.2.2", True),
        (schemas.Package(ecosystem="PyPI", name="Plone"), "5.2.3", False),
        (schemas.Package(ecosystem="PyPI", name="plone.app.event"), "3.2.9", True),
        (schemas.Package(ecosystem="PyPI", name="plone.app.event"), "3.2.10", False),
    ],
)
def test_is_affected_package_version_with_multiple_package(
    vuln: schemas.Vulnerability,
    package: schemas.Package,
    version: str,
    expected: bool,
):
    assert (
        vuln.is_affected_package_version(version=version, package=package) is expected
    )
