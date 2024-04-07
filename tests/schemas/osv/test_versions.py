import pytest

from mihama import schemas


@pytest.fixture()
def vuln():
    # versions: 3.2 to 5.2rc5
    with open("tests/fixtures/advisories/versions.json") as f:
        return schemas.Vulnerability.model_validate_json(f.read())


@pytest.mark.parametrize(
    ("package", "version", "expected"),
    [
        (schemas.Package(ecosystem="PyPI", name="plone"), "3.1", False),
        (schemas.Package(ecosystem="PyPI", name="plone"), "3.2", True),
        (schemas.Package(ecosystem="PyPI", name="plone"), "5.2rc5", True),
        (schemas.Package(ecosystem="PyPI", name="plone"), "6.0", False),
        (schemas.Package(ecosystem="PyPI", name="dummy"), "3.2", False),
        (schemas.Package(ecosystem="PyPI", name="dummy"), "5.2rc5", False),
    ],
)
def test_is_affected_package_version_with_versions(
    vuln: schemas.Vulnerability,
    package: schemas.Package,
    version: str,
    expected: bool,
):
    assert (
        vuln.is_affected_package_version(version=version, package=package) is expected
    )
