from src.rema.json_dtos.department_dto import (
    DepartmentCategoryDto,
    Extra,
    RemaDepartmentDto,
)


class DepartmentDtoBuilder:
    def __init__(self) -> None:
        self.categories = []
        self.id = 1

    def with_categories(self, categories: list[DepartmentCategoryDto]):
        self.categories = categories
        return self

    def with_id(self, id: int):
        self.id = id
        return self

    def build(self):
        return RemaDepartmentDto(
            id=1,
            name="",
            slug="",
            categories=self.categories,
            extra=ExtraBuilder().build(),
        )


class ExtraBuilder:
    def build(self):
        return Extra(
            modules=[],
        )


class DepartmentCategoryDtoBuilder:
    def __init__(self) -> None:
        self.id = 1

    def with_id(self, id: int):
        self.id = id
        return self

    def build(self):
        return DepartmentCategoryDto(
            id=self.id,
            name="",
            slug="",
            hidden=False,
        )
