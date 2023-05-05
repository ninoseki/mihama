import vcr

from mihama.core.settings.osv import get_osv_ecosystems


@vcr.use_cassette("tests/fixtures/vcr_cassettes/ecosystems.yaml")  # type: ignore
def test_get_osv_ecosystems():
    assert "npm" in get_osv_ecosystems()
