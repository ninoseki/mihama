import abc
from typing import Any, get_args, get_origin

from aredis_om.model.model import NUMERIC_TYPES, SINGLE_VALUE_TAG_FIELD_SEPARATOR
from aredis_om.model.model import JsonModel as JsonModel_
from aredis_om.model.model import (
    RedisModel,
    RedisModelError,
    is_supported_container_type,
    log,
)
from pydantic.fields import FieldInfo as PydanticFieldInfo


class JsonModel(JsonModel_):
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
        should_index = getattr(field_info, "index", False)
        is_container_type = is_supported_container_type(typ)
        parent_is_container_type = is_supported_container_type(parent_type)
        parent_is_model = False

        if parent_type:
            try:
                parent_is_model = issubclass(parent_type, RedisModel)
            except TypeError:
                pass

        # TODO: We need a better way to know that we're indexing a value
        #  discovered in a model within an array.
        #
        # E.g., say we have a field like `orders: List[Order]`, and we're
        # indexing the "name" field from the Order model (because it's marked
        # index=True in the Order model). The JSONPath for this field is
        # $.orders[*].name, but the "parent" type at this point is Order, not
        # List. For now, we'll discover that Orders are stored in a list by
        # checking if the JSONPath contains the expression for all items in
        # an array.
        parent_is_model_in_container = parent_is_model and json_path.endswith("[*]")

        try:
            field_is_model = issubclass(typ, RedisModel)
        except TypeError:
            # Not a class, probably a type annotation
            field_is_model = False

        # When we encounter a list or model field, we need to descend
        # into the values of the list or the fields of the model to
        # find any values marked as indexed.
        if is_container_type:
            field_type = get_origin(typ)
            embedded_cls = get_args(typ)
            if not embedded_cls:
                log.warning(
                    "Model %s defined an empty list or tuple field: %s", cls, name
                )
                return ""
            embedded_cls = embedded_cls[0]
            return cls.schema_for_type(
                f"{json_path}.{name}[*]",
                name,
                name_prefix,
                embedded_cls,
                field_info,
                parent_type=field_type,
            )
        elif field_is_model:
            name_prefix = f"{name_prefix}_{name}" if name_prefix else name
            sub_fields = []
            for embedded_name, field in typ.__fields__.items():
                if parent_is_container_type:
                    # We'll store this value either as a JavaScript array, so
                    # the correct JSONPath expression is to refer directly to
                    # attribute names after the container notation, e.g.
                    # orders[*].created_date.
                    path = json_path
                else:
                    # All other fields should use dot notation with both the
                    # current field name and "embedded" field name, e.g.,
                    # order.address.street_line_1.
                    path = f"{json_path}.{name}"
                sub_fields.append(
                    cls.schema_for_type(
                        path,
                        embedded_name,
                        name_prefix,
                        field.outer_type_,
                        field.field_info,
                        parent_type=typ,
                    )
                )
            return " ".join(filter(None, sub_fields))
        # NOTE: This is the termination point for recursion. We've descended
        # into models and lists until we found an actual value to index.
        elif should_index:
            index_field_name = f"{name_prefix}_{name}" if name_prefix else name
            if parent_is_container_type:
                # If we're indexing the this field as a JavaScript array, then
                # the currently built-up JSONPath expression will be
                # "field_name[*]", which is what we want to use.
                path = json_path
            else:
                path = f"{json_path}.{name}"
            sortable = getattr(field_info, "sortable", False)
            full_text_search = getattr(field_info, "full_text_search", False)
            sortable_tag_error = RedisModelError(
                "In this Preview release, TAG fields cannot "
                f"be marked as sortable. Problem field: {name}. "
                "See docs: TODO"
            )

            # TODO: GEO field
            if parent_is_container_type or parent_is_model_in_container:
                if typ is not str:
                    raise RedisModelError(
                        "In this Preview release, list and tuple fields can only "
                        f"contain strings. Problem field: {name}. See docs: TODO"
                    )
                if full_text_search is True:
                    raise RedisModelError(
                        "List and tuple fields cannot be indexed for full-text "
                        f"search. Problem field: {name}. See docs: TODO"
                    )
                schema = f"{path} AS {index_field_name} TAG SEPARATOR {SINGLE_VALUE_TAG_FIELD_SEPARATOR}"

                if sortable is True:
                    raise sortable_tag_error
            elif any(issubclass(typ, t) for t in NUMERIC_TYPES):
                schema = f"{path} AS {index_field_name} NUMERIC"
            elif issubclass(typ, str):
                if full_text_search is True:
                    schema = (
                        f"{path} AS {index_field_name} TAG SEPARATOR {SINGLE_VALUE_TAG_FIELD_SEPARATOR} CASESENSITIVE"
                        f"{path} AS {index_field_name}_fts TEXT"
                    )
                    if sortable is True:
                        # NOTE: With the current preview release, making a field
                        # full-text searchable and sortable only makes the TEXT
                        # field sortable. This means that results for full-text
                        # search queries can be sorted, but not exact match
                        # queries.
                        schema += " SORTABLE"
                else:
                    schema = f"{path} AS {index_field_name} TAG SEPARATOR {SINGLE_VALUE_TAG_FIELD_SEPARATOR}"

                if index_field_name != "pk" and "CASESENSITIVE" not in schema:
                    schema += " CASESENSITIVE"

                if sortable is True:
                    raise sortable_tag_error
            else:
                schema = f"{path} AS {index_field_name} TAG SEPARATOR {SINGLE_VALUE_TAG_FIELD_SEPARATOR}"
                if sortable is True:
                    raise sortable_tag_error
            return schema
        return ""


class EmbeddedJsonModel(JsonModel, abc.ABC):
    class Meta:
        embedded = True
