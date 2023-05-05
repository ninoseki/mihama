import requests

from mihama.core.datastructures import UniqueCommaSeparatedStrings

from .config import config

DEFAULT_OSV_ECOSYSTEMS = UniqueCommaSeparatedStrings(
    [
        "AlmaLinux",
        "AlmaLinux:8",
        "AlmaLinux:9",
        "Alpine",
        "Alpine:v3.10",
        "Alpine:v3.11",
        "Alpine:v3.12",
        "Alpine:v3.13",
        "Alpine:v3.14",
        "Alpine:v3.15",
        "Alpine:v3.16",
        "Alpine:v3.17",
        "Alpine:v3.2",
        "Alpine:v3.3",
        "Alpine:v3.4",
        "Alpine:v3.5",
        "Alpine:v3.6",
        "Alpine:v3.7",
        "Alpine:v3.8",
        "Alpine:v3.9",
        "Android",
        "Debian",
        "Debian:10",
        "Debian:11",
        "Debian:3.0",
        "Debian:3.1",
        "Debian:4.0",
        "Debian:5.0",
        "Debian:6.0",
        "Debian:7",
        "Debian:8",
        "Debian:9",
        "GSD",
        "GitHub Actions",
        "Go",
        "Hex",
        "Linux",
        "Maven",
        "NuGet",
        "OSS-Fuzz",
        "Packagist",
        "Pub",
        "PyPI",
        "Rocky Linux",
        "Rocky Linux:8",
        "Rocky Linux:9",
        "RubyGems",
        "UVI",
        "crates.io",
        "npm",
    ]
)


def get_osv_ecosystems(
    url: str = "https://osv-vulnerabilities.storage.googleapis.com/ecosystems.txt",
    *,
    default=DEFAULT_OSV_ECOSYSTEMS
) -> UniqueCommaSeparatedStrings:
    try:
        res = requests.get(url)
        res.raise_for_status()

        text = res.text
        return UniqueCommaSeparatedStrings([line.strip() for line in text.splitlines()])
    except requests.HTTPError:
        return default


OSV_BUCKET_BASE_URL: str = config(
    "OSV_BUCKET_BASE_URL",
    cast=str,
    default="https://osv-vulnerabilities.storage.googleapis.com",
)

OSV_ECOSYSTEMS: UniqueCommaSeparatedStrings = config(
    "OSV_ECOSYSTEMS",
    cast=UniqueCommaSeparatedStrings,
    default=get_osv_ecosystems(),
)

OSV_BUCKET_TIMEOUT: int = config(
    "OSV_BUCKET_TIMEOUT",
    cast=int,
    default=180,
)

OSV_QUERY_BATCH_MAX_AT_ONCE: int = config(
    "OSV_QUERY_BATCH_MAX_AT_ONCE",
    cast=int,
    default=100,
)
