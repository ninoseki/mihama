from starlette.datastructures import CommaSeparatedStrings

from .config import config

OSV_BUCKET_BASE_URL: str = config(
    "OSV_BUCKET_BASE_URL",
    cast=str,
    default="https://osv-vulnerabilities.storage.googleapis.com",
)

OSV_ECOSYSTEMS: CommaSeparatedStrings = config(
    "OSV_ECOSYSTEMS",
    cast=CommaSeparatedStrings,
    default="npm,Maven,Go,NuGet,PyPI,RubyGems,crates.io,Packagist,Linux,OSS-Fuzz",
)

OSV_BUCKET_DOWNLOAD_TIMEOUT: int = config(
    "OSV_BUCKET_DOWNLOAD_TIMEOUT",
    cast=int,
    default=180,
)

OSV_QUERY_BATCH_MAX_AT_ONCE: int = config(
    "OSV_QUERY_BATCH_MAX_AT_ONCE",
    cast=int,
    default=100,
)
