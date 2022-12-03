import pytest

from mihama import models


@pytest.fixture
def vulnerability_with_semver():
    # introduced: 0
    # fixed: 0.0.9
    return models.Vulnerability.parse_file(
        "tests/fixtures/advisories/GHSA-2hfj-cxw7-g45p.json"
    )


def test_post_init_timestamp_creation(vulnerability_with_semver: models.Vulnerability):
    assert vulnerability_with_semver.timestamp is not None
    assert (
        vulnerability_with_semver.timestamp
        == vulnerability_with_semver.modified.timestamp()
    )


@pytest.mark.parametrize(
    "version,expected", [("0.0.8", True), ("0.0.9", False), ("1.0.0", False)]
)
def test_is_affected_version_vulnerability_with_semver(
    vulnerability_with_semver: models.Vulnerability, version: str, expected: bool
):
    assert vulnerability_with_semver.is_affected_version(version) is expected


@pytest.fixture
def vulnerability_with_versions():
    return models.Vulnerability.parse_file(
        "tests/fixtures/advisories/GHSA-2c8c-84w2-j38j.json"
    )


@pytest.mark.parametrize(
    "version,expected", [("0.1", False), ("3.0", True), ("4.0", True), ("100.0", False)]
)
def test_is_affected_version_vulnerability_with_versions(
    vulnerability_with_versions: models.Vulnerability, version: str, expected: bool
):
    assert vulnerability_with_versions.is_affected_version(version) is expected
