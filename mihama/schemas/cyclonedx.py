from pydantic import BaseModel, Field

from .osv import BatchQuery, Package, Query


class Component(BaseModel):
    purl: str | None = Field(None, description="Specifies the package-url (purl)")
    components: list["Component"] = Field(
        default_factory=list, description="A list of software and hardware component"
    )

    def get_flatten_components(
        self,
    ) -> list["Component"]:
        flatten: list["Component"] = []
        flatten.append(self)

        for c in self.components:
            flatten.extend(c.get_flatten_components())

        return flatten

    def to_query(self) -> Query | None:
        if self.purl is None:
            return None

        return Query(package=Package(purl=self.purl))


class CycloneDX(BaseModel):
    components: list[Component] = Field(
        default_factory=list, description="A list of software and hardware component"
    )

    def to_batch_query(self) -> BatchQuery:
        components: list[Component] = []
        for c in self.components:
            components.extend(c.get_flatten_components())

        queries = [c.to_query() for c in components]
        return BatchQuery(queries=[q for q in queries if q is not None])
