from starlette.datastructures import CommaSeparatedStrings, Secret

from mihama.utils import cast_csv
from mihama.version import __version__

from .config import config

ES_HOSTS = cast_csv(
    config("ES_HOSTS", cast=CommaSeparatedStrings, default="http://localhost:9200"),  # type: ignore
    cast=str,
)
ES_USERNAME: str = config("ES_USERNAME", cast=str, default="elastic")
ES_PASSWORD: Secret = config("ES_PASSWORD", cast=Secret, default="changeme")  # type: ignore

ES_INDEX: str = config("ES_INDEX", cast=str, default=f"mihama-v{__version__}")
