import typing

from starlette.datastructures import CommaSeparatedStrings


class UniqueCommaSeparatedStrings(CommaSeparatedStrings):
    def __init__(self, value: str | typing.Sequence[str]):
        super().__init__(value)

        self._items = list(set(self._items))
