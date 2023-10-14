from .config import config

OSSF_MALICIOUS_PACKAGES_REPO_URL: str = config(
    "OSSF_MALICIOUS_PACKAGES_REPO_URL",
    cast=str,
    default="https://github.com/ossf/malicious-packages",
)

ENABLE_OSSF_MALICIOUS_PACKAGES: bool = config(
    "ENABLE_OSSF_MALICIOUS_PACKAGES",
    cast=bool,
    default=True,
)
