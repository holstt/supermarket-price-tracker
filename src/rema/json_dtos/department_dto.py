from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class DepartmentCategoryDto:
    id: int
    name: str
    slug: str
    hidden: bool

    @staticmethod
    def from_dict(obj: Any) -> 'DepartmentCategoryDto':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        slug = from_str(obj.get("slug"))
        hidden = from_bool(obj.get("hidden"))
        return DepartmentCategoryDto(id, name, slug, hidden)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["slug"] = from_str(self.slug)
        result["hidden"] = from_bool(self.hidden)
        return result


@dataclass
class Extra:
    modules: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'Extra':
        assert isinstance(obj, dict)
        modules = from_list(lambda x: x, obj.get("modules"))
        return Extra(modules)

    def to_dict(self) -> dict:
        result: dict = {}
        result["modules"] = from_list(lambda x: x, self.modules)
        return result


@dataclass
class RemaDepartmentDto:
    id: int
    name: str
    slug: str
    categories: List[DepartmentCategoryDto]
    extra: Extra

    @staticmethod
    def from_dict(obj: Any) -> 'RemaDepartmentDto':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        slug = from_str(obj.get("slug"))
        categories = from_list(
            DepartmentCategoryDto.from_dict, obj.get("categories"))
        extra = Extra.from_dict(obj.get("extra"))
        return RemaDepartmentDto(id, name, slug, categories, extra)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["slug"] = from_str(self.slug)
        result["categories"] = from_list(
            lambda x: to_class(DepartmentCategoryDto, x), self.categories)
        result["extra"] = to_class(Extra, self.extra)
        return result


def departments_dto_from_json(s: Any) -> List[RemaDepartmentDto]:
    return from_list(RemaDepartmentDto.from_dict, s)
