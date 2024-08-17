import pytest

from mihama import schemas


@pytest.fixture
def vuln():
    # introduced: 0
    # fixed: 0.0.9
    with open("tests/fixtures/advisories/fixed.json") as f:
        return schemas.Vulnerability.model_validate_json(f.read())


@pytest.mark.parametrize(
    ("package", "version", "expected"),
    [
        (
            schemas.Package(ecosystem="Go", name="github.com/owncast/owncast"),
            "0.0.8",
            True,
        ),
        (
            schemas.Package(ecosystem="Go", name="github.com/owncast/owncast"),
            "0.0.9",
            False,
        ),
        (schemas.Package(ecosystem="Go", name="dummy"), "0.0.8", False),
    ],
)
def test_is_affected_package_version_with_fixed(
    vuln: schemas.Vulnerability,
    package: schemas.Package,
    version: str,
    expected: bool,
):
    assert (
        vuln.is_affected_package_version(version=version, package=package) is expected
    )
