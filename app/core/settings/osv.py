from app.core.datastructures import UniqueCommaSeparatedStrings

from .config import config

OSV_BUCKET_BASE_URL: str = config(
    "OSV_BUCKET_BASE_URL",
    cast=str,
    default="https://osv-vulnerabilities.storage.googleapis.com",
)

OSV_ECOSYSTEMS: UniqueCommaSeparatedStrings = config(
    "OSV_ECOSYSTEMS",
    cast=UniqueCommaSeparatedStrings,
    default="npm,Maven,Go,NuGet,PyPI,RubyGems,crates.io,Packagist,Linux,OSS-Fuzz,Alpine,Android,Debian,DWF,GitHub Actions,GSD,Hex,JavaScript,Pub,UVI",
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
