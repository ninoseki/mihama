import pytest

from mihama import schemas


@pytest.fixture()
def vuln():
    # introduced: 0
    # last_affected: 4.1.0
    with open("tests/fixtures/advisories/last_affected.json") as f:
        return schemas.Vulnerability.model_validate_json(f.read())


@pytest.mark.parametrize(
    ("package", "version", "expected"),
    [
        (schemas.Package(ecosystem="PyPI", name="opencv-python"), "4.1.0", True),
        (schemas.Package(ecosystem="PyPI", name="opencv-python"), "4.1.1", False),
        (schemas.Package(ecosystem="PyPI", name="dummy"), "4.1.0", False),
    ],
)
def test_is_affected_package_version_with_last_affected(
    vuln: schemas.Vulnerability,
    package: schemas.Package,
    version: str,
    expected: bool,
):
    assert (
        vuln.is_affected_package_version(version=version, package=package) is expected
    )
