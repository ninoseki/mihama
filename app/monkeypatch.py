import re
from re import Pattern

import aredis_om.model.model


class TokenEscaper:
    """
    Escape punctuation within an input string.
    """

    # Characters that RediSearch requires us to escape during queries.
    # Source: https://oss.redis.com/redisearch/Escaping/#the_rules_of_text_field_tokenization
    DEFAULT_ESCAPED_CHARS = r"[,.<>{}\[\]\\\"\':;!@#$%^&*()\-+=~\/ ]"

    def __init__(self, escape_chars_re: Pattern | None = None):
        if escape_chars_re:
            self.escaped_chars_re = escape_chars_re
        else:
            self.escaped_chars_re = re.compile(self.DEFAULT_ESCAPED_CHARS)

    def escape(self, value: str) -> str:
        def escape_symbol(match):
            value = match.group(0)
            return f"\\{value}"

        return self.escaped_chars_re.sub(escape_symbol, value)


def monkeypatch_escaper():
    # apply this fix
    # https://github.com/redis/redis-om-python/pull/376
    aredis_om.model.model.escaper = TokenEscaper()
