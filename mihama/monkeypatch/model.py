import abc
from typing import Any

from aredis_om.model import model
from pydantic.fields import FieldInfo as PydanticFieldInfo


class JsonModel(model.JsonModel):
    @classmethod
    def schema_for_type(
        cls,
        json_path: str,
        name: str,
        name_prefix: str,
        typ: Any,
        field_info: PydanticFieldInfo,
        parent_type: Any | None = None,
    ) -> str:
        schema = super().schema_for_type(
            json_path, name, name_prefix, typ, field_info, parent_type
        )

        if not issubclass(typ, str):
            return schema

        schema = schema.strip()
        if schema == "":
            return schema

        # make it case sensitive
        index_field_name = f"{name_prefix}_{name}" if name_prefix else name

        is_pk = index_field_name == "pk" or index_field_name.endswith("_pk")
        is_case_sensitive = "CASESENSITIVE" in schema
        if not is_pk and not is_case_sensitive:
            schema += " CASESENSITIVE"

        return schema


class EmbeddedJsonModel(JsonModel, abc.ABC):
    class Meta:
        embedded = True
