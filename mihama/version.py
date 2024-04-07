import os

import tomllib


def get_version():
    path = os.path.join(os.path.dirname(__file__), "../pyproject.toml")
    with open(path) as f:
        parsed = tomllib.loads(f.read())

    return parsed.get("tool", {}).get("poetry", {}).get("version", "0.0.0")


__version__ = get_version()
