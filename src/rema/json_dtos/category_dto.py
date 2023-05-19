# type: ignore


from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

import dateutil.parser

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


@dataclass
class Exhaustive:
    facets_count: Optional[bool] = None
    nb_hits: Optional[bool] = None
    typo: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Exhaustive':
        assert isinstance(obj, dict)
        facets_count = from_union(
            [from_bool, from_none], obj.get("facetsCount"))
        nb_hits = from_union([from_bool, from_none], obj.get("nbHits"))
        typo = from_union([from_bool, from_none], obj.get("typo"))
        return Exhaustive(facets_count, nb_hits, typo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.facets_count is not None:
            result["facetsCount"] = from_union(
                [from_bool, from_none], self.facets_count)
        if self.nb_hits is not None:
            result["nbHits"] = from_union([from_bool, from_none], self.nb_hits)
        if self.typo is not None:
            result["typo"] = from_union([from_bool, from_none], self.typo)
        return result


@dataclass
class Labels:
    keyhole: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Labels':
        assert isinstance(obj, dict)
        keyhole = from_union([from_int, from_none], obj.get("keyhole"))
        return Labels(keyhole)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.keyhole is not None:
            result["keyhole"] = from_union([from_int, from_none], self.keyhole)
        return result


@dataclass
class Facets:
    labels: Optional[Labels] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Facets':
        assert isinstance(obj, dict)
        labels = from_union([Labels.from_dict, from_none], obj.get("labels"))
        return Facets(labels)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.labels is not None:
            result["labels"] = from_union(
                [lambda x: to_class(Labels, x), from_none], self.labels)
        return result


class CategoryNameEnum(Enum):
    BAVINCHI_BAGER = "Bavinchi bager"
    FAST_FOOD_BRØD = "Fast food brød"
    RUGBRØD = "Rugbrød"


class DepartmentName(Enum):
    BRØD_BAVINCHI = "Brød & Bavinchi"


@dataclass
class Extra:
    video: None
    extended_description: None
    popularity: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Extra':
        assert isinstance(obj, dict)
        video = from_none(obj.get("video"))
        extended_description = from_none(obj.get("extended_description"))
        popularity = from_union([from_int, from_none], obj.get("popularity"))
        return Extra(video, extended_description, popularity)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.video is not None:
            result["video"] = from_none(self.video)
        if self.extended_description is not None:
            result["extended_description"] = from_none(
                self.extended_description)
        if self.popularity is not None:
            result["popularity"] = from_union(
                [from_int, from_none], self.popularity)
        return result


class MatchLevel(Enum):
    NONE = "none"


@dataclass
class CategoryNameClass:
    value: Optional[str] = None
    match_level: Optional[MatchLevel] = None
    matched_words: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryNameClass':
        assert isinstance(obj, dict)
        value = from_union([from_str, from_none], obj.get("value"))
        match_level = from_union(
            [MatchLevel, from_none], obj.get("matchLevel"))
        matched_words = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("matchedWords"))
        return CategoryNameClass(value, match_level, matched_words)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.value is not None:
            result["value"] = from_union([from_str, from_none], self.value)
        if self.match_level is not None:
            result["matchLevel"] = from_union(
                [lambda x: to_enum(MatchLevel, x), from_none], self.match_level)
        if self.matched_words is not None:
            result["matchedWords"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.matched_words)
        return result


@dataclass
class HighlightResult:
    id: Optional[CategoryNameClass] = None
    name: Optional[CategoryNameClass] = None
    hf2: Optional[CategoryNameClass] = None
    category_name: Optional[CategoryNameClass] = None
    labels: Optional[List[CategoryNameClass]] = None
    search_words: Optional[List[CategoryNameClass]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'HighlightResult':
        assert isinstance(obj, dict)
        id = from_union([CategoryNameClass.from_dict,
                        from_none], obj.get("id"))
        name = from_union([CategoryNameClass.from_dict,
                          from_none], obj.get("name"))
        hf2 = from_union([CategoryNameClass.from_dict,
                         from_none], obj.get("hf2"))
        category_name = from_union(
            [CategoryNameClass.from_dict, from_none], obj.get("category_name"))
        labels = from_union([lambda x: from_list(
            CategoryNameClass.from_dict, x), from_none], obj.get("labels"))
        search_words = from_union([lambda x: from_list(
            CategoryNameClass.from_dict, x), from_none], obj.get("search_words"))
        return HighlightResult(id, name, hf2, category_name, labels, search_words)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union(
                [lambda x: to_class(CategoryNameClass, x), from_none], self.id)
        if self.name is not None:
            result["name"] = from_union(
                [lambda x: to_class(CategoryNameClass, x), from_none], self.name)
        if self.hf2 is not None:
            result["hf2"] = from_union(
                [lambda x: to_class(CategoryNameClass, x), from_none], self.hf2)
        if self.category_name is not None:
            result["category_name"] = from_union(
                [lambda x: to_class(CategoryNameClass, x), from_none], self.category_name)
        if self.labels is not None:
            result["labels"] = from_union([lambda x: from_list(
                lambda x: to_class(CategoryNameClass, x), x), from_none], self.labels)
        if self.search_words is not None:
            result["search_words"] = from_union([lambda x: from_list(
                lambda x: to_class(CategoryNameClass, x), x), from_none], self.search_words)
        return result


class MedianWeightUnit(Enum):
    GRAM = "gram"


class Name(Enum):
    ENERGI = "Energi"
    FEDT = "Fedt"
    HERAF_MÆTTEDE_FEDTSYRER = "Heraf mættede fedtsyrer"
    HERAF_SUKKERARTER = "Heraf sukkerarter"
    KOSTFIBRE = "Kostfibre"
    KULHYDRAT = "Kulhydrat"
    PROTEIN = "Protein"
    SALT = "Salt"


@dataclass
class NutritionInfo:
    sort: Optional[int] = None
    name: Optional[Name] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'NutritionInfo':
        assert isinstance(obj, dict)
        sort = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("sort"))
        name = from_union([Name, from_none], obj.get("name"))
        value = from_union([from_str, from_none], obj.get("value"))
        return NutritionInfo(sort, name, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.sort is not None:
            result["sort"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(
                x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.sort)
        if self.name is not None:
            result["name"] = from_union(
                [lambda x: to_enum(Name, x), from_none], self.name)
        if self.value is not None:
            result["value"] = from_union([from_str, from_none], self.value)
        return result


@dataclass
class Pricing:
    price: Optional[float] = None
    max_quantity: Optional[int] = None
    price_over_max: Optional[float] = None
    is_on_discount: Optional[bool] = None
    normal_price: Optional[float] = None
    price_per_kilogram: Optional[float] = None
    price_per_unit: Optional[str] = None
    price_changes_on: Optional[datetime] = None
    price_changes_type: Optional[str] = None
    is_advertised: Optional[bool] = None
    deposit: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Pricing':
        assert isinstance(obj, dict)
        price = from_union([from_float, from_none], obj.get("price"))
        max_quantity = from_union(
            [from_int, from_none], obj.get("max_quantity"))
        price_over_max = from_union(
            [from_float, from_none], obj.get("price_over_max"))
        is_on_discount = from_union(
            [from_bool, from_none], obj.get("is_on_discount"))
        normal_price = from_union(
            [from_float, from_none], obj.get("normal_price"))
        price_per_kilogram = from_union(
            [from_float, from_none], obj.get("price_per_kilogram"))
        price_per_unit = from_union(
            [from_str, from_none], obj.get("price_per_unit"))
        price_changes_on = from_union(
            [from_none, from_datetime], obj.get("price_changes_on"))
        price_changes_type = from_union(
            [from_none, from_str], obj.get("price_changes_type"))
        is_advertised = from_union(
            [from_bool, from_none], obj.get("is_advertised"))
        deposit = from_union([from_int, from_none], obj.get("deposit"))
        return Pricing(price, max_quantity, price_over_max, is_on_discount, normal_price, price_per_kilogram, price_per_unit, price_changes_on, price_changes_type, is_advertised, deposit)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.price is not None:
            result["price"] = from_union([to_float, from_none], self.price)
        if self.max_quantity is not None:
            result["max_quantity"] = from_union(
                [from_int, from_none], self.max_quantity)
        if self.price_over_max is not None:
            result["price_over_max"] = from_union(
                [to_float, from_none], self.price_over_max)
        if self.is_on_discount is not None:
            result["is_on_discount"] = from_union(
                [from_bool, from_none], self.is_on_discount)
        if self.normal_price is not None:
            result["normal_price"] = from_union(
                [to_float, from_none], self.normal_price)
        if self.price_per_kilogram is not None:
            result["price_per_kilogram"] = from_union(
                [to_float, from_none], self.price_per_kilogram)
        if self.price_per_unit is not None:
            result["price_per_unit"] = from_union(
                [from_str, from_none], self.price_per_unit)
        if self.price_changes_on is not None:
            result["price_changes_on"] = from_union(
                [from_none, lambda x: x.isoformat()], self.price_changes_on)
        if self.price_changes_type is not None:
            result["price_changes_type"] = from_union(
                [from_none, from_str], self.price_changes_type)
        if self.is_advertised is not None:
            result["is_advertised"] = from_union(
                [from_bool, from_none], self.is_advertised)
        if self.deposit is not None:
            result["deposit"] = from_union([from_int, from_none], self.deposit)
        return result


@dataclass
class Hit:
    min_age: None
    item_label: None
    item_disclaimer: None
    temperature_zone: None
    object_id: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    underline: Optional[str] = None
    hf2: Optional[str] = None
    country_of_origin_code: Optional[str] = None
    pricing: Optional[Pricing] = None
    labels: Optional[List[str]] = None
    wine_type_labels: Optional[List[Any]] = None
    season_labels: Optional[List[Any]] = None
    review_labels: Optional[List[Any]] = None
    fits_with_labels: Optional[List[Any]] = None
    description: Optional[str] = None
    description_short: Optional[str] = None
    hp_statements: Optional[List[Any]] = None
    declaration: Optional[str] = None
    declaration_old: Optional[str] = None
    nutrition_info: Optional[List[NutritionInfo]] = None
    nutrition_info_old: Optional[List[Any]] = None
    image_url: Optional[str] = None
    have_image: Optional[bool] = None
    bar_codes: Optional[List[str]] = None
    search_words: Optional[List[str]] = None
    sorting: Optional[int] = None
    is_weight_item: Optional[bool] = None
    median_weight: Optional[int] = None
    median_weight_unit: Optional[MedianWeightUnit] = None
    is_self_scale_item: Optional[bool] = None
    assortment_code: Optional[int] = None
    assortment_disclaimer: Optional[str] = None
    assortment_label: Optional[str] = None
    extra: Optional[Extra] = None
    warnings: Optional[List[Any]] = None
    department_id: Optional[int] = None
    department_name: Optional[DepartmentName] = None
    category_id: Optional[int] = None
    category_name: Optional[CategoryNameEnum] = None
    modified_at: Optional[int] = None
    highlight_result: Optional[HighlightResult] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Hit':
        assert isinstance(obj, dict)
        min_age = from_none(obj.get("min_age"))
        item_label = from_none(obj.get("item_label"))
        item_disclaimer = from_none(obj.get("item_disclaimer"))
        temperature_zone = from_none(obj.get("temperature_zone"))
        object_id = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("objectID"))
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        underline = from_union([from_str, from_none], obj.get("underline"))
        hf2 = from_union([from_str, from_none], obj.get("hf2"))
        country_of_origin_code = from_union(
            [from_str, from_none], obj.get("country_of_origin_code"))
        pricing = from_union(
            [Pricing.from_dict, from_none], obj.get("pricing"))
        labels = from_union([lambda x: from_list(
            from_str, x), from_none], obj.get("labels"))
        wine_type_labels = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("wine_type_labels"))
        season_labels = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("season_labels"))
        review_labels = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("review_labels"))
        fits_with_labels = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("fits_with_labels"))
        description = from_union([from_str, from_none], obj.get("description"))
        description_short = from_union(
            [from_str, from_none], obj.get("description_short"))
        hp_statements = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("hp_statements"))
        declaration = from_union([from_str, from_none], obj.get("declaration"))
        declaration_old = from_union(
            [from_str, from_none], obj.get("declaration_old"))
        nutrition_info = from_union([lambda x: from_list(
            NutritionInfo.from_dict, x), from_none], obj.get("nutrition_info"))
        nutrition_info_old = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("nutrition_info_old"))
        image_url = from_union([from_str, from_none], obj.get("image_url"))
        have_image = from_union([from_bool, from_none], obj.get("have_image"))
        bar_codes = from_union([lambda x: from_list(
            from_str, x), from_none], obj.get("bar_codes"))
        search_words = from_union([lambda x: from_list(
            from_str, x), from_none], obj.get("search_words"))
        sorting = from_union([from_int, from_none], obj.get("sorting"))
        is_weight_item = from_union(
            [from_bool, from_none], obj.get("is_weight_item"))
        median_weight = from_union(
            [from_int, from_none], obj.get("median_weight"))
        median_weight_unit = from_union(
            [MedianWeightUnit, from_none], obj.get("median_weight_unit"))
        is_self_scale_item = from_union(
            [from_bool, from_none], obj.get("is_self_scale_item"))
        assortment_code = from_union(
            [from_int, from_none], obj.get("assortment_code"))
        assortment_disclaimer = from_union(
            [from_none, from_str], obj.get("assortment_disclaimer"))
        assortment_label = from_union(
            [from_none, from_str], obj.get("assortment_label"))
        extra = from_union([Extra.from_dict, from_none], obj.get("extra"))
        warnings = from_union([lambda x: from_list(
            lambda x: x, x), from_none], obj.get("warnings"))
        department_id = from_union(
            [from_int, from_none], obj.get("department_id"))
        department_name = from_union(
            [DepartmentName, from_none], obj.get("department_name"))
        category_id = from_union([from_int, from_none], obj.get("category_id"))
        category_name = from_union(
            [CategoryNameEnum, from_none], obj.get("category_name"))
        modified_at = from_union([from_int, from_none], obj.get("modified_at"))
        highlight_result = from_union(
            [HighlightResult.from_dict, from_none], obj.get("_highlightResult"))
        return Hit(min_age, item_label, item_disclaimer, temperature_zone, object_id, id, name, underline, hf2, country_of_origin_code, pricing, labels, wine_type_labels, season_labels, review_labels, fits_with_labels, description, description_short, hp_statements, declaration, declaration_old, nutrition_info, nutrition_info_old, image_url, have_image, bar_codes, search_words, sorting, is_weight_item, median_weight, median_weight_unit, is_self_scale_item, assortment_code, assortment_disclaimer, assortment_label, extra, warnings, department_id, department_name, category_id, category_name, modified_at, highlight_result)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.min_age is not None:
            result["min_age"] = from_none(self.min_age)
        if self.item_label is not None:
            result["item_label"] = from_none(self.item_label)
        if self.item_disclaimer is not None:
            result["item_disclaimer"] = from_none(self.item_disclaimer)
        if self.temperature_zone is not None:
            result["temperature_zone"] = from_none(self.temperature_zone)
        if self.object_id is not None:
            result["objectID"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(
                x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.object_id)
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.underline is not None:
            result["underline"] = from_union(
                [from_str, from_none], self.underline)
        if self.hf2 is not None:
            result["hf2"] = from_union([from_str, from_none], self.hf2)
        if self.country_of_origin_code is not None:
            result["country_of_origin_code"] = from_union(
                [from_str, from_none], self.country_of_origin_code)
        if self.pricing is not None:
            result["pricing"] = from_union(
                [lambda x: to_class(Pricing, x), from_none], self.pricing)
        if self.labels is not None:
            result["labels"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.labels)
        if self.wine_type_labels is not None:
            result["wine_type_labels"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.wine_type_labels)
        if self.season_labels is not None:
            result["season_labels"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.season_labels)
        if self.review_labels is not None:
            result["review_labels"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.review_labels)
        if self.fits_with_labels is not None:
            result["fits_with_labels"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.fits_with_labels)
        if self.description is not None:
            result["description"] = from_union(
                [from_str, from_none], self.description)
        if self.description_short is not None:
            result["description_short"] = from_union(
                [from_str, from_none], self.description_short)
        if self.hp_statements is not None:
            result["hp_statements"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.hp_statements)
        if self.declaration is not None:
            result["declaration"] = from_union(
                [from_str, from_none], self.declaration)
        if self.declaration_old is not None:
            result["declaration_old"] = from_union(
                [from_str, from_none], self.declaration_old)
        if self.nutrition_info is not None:
            result["nutrition_info"] = from_union([lambda x: from_list(
                lambda x: to_class(NutritionInfo, x), x), from_none], self.nutrition_info)
        if self.nutrition_info_old is not None:
            result["nutrition_info_old"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.nutrition_info_old)
        if self.image_url is not None:
            result["image_url"] = from_union(
                [from_str, from_none], self.image_url)
        if self.have_image is not None:
            result["have_image"] = from_union(
                [from_bool, from_none], self.have_image)
        if self.bar_codes is not None:
            result["bar_codes"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.bar_codes)
        if self.search_words is not None:
            result["search_words"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.search_words)
        if self.sorting is not None:
            result["sorting"] = from_union([from_int, from_none], self.sorting)
        if self.is_weight_item is not None:
            result["is_weight_item"] = from_union(
                [from_bool, from_none], self.is_weight_item)
        if self.median_weight is not None:
            result["median_weight"] = from_union(
                [from_int, from_none], self.median_weight)
        if self.median_weight_unit is not None:
            result["median_weight_unit"] = from_union(
                [lambda x: to_enum(MedianWeightUnit, x), from_none], self.median_weight_unit)
        if self.is_self_scale_item is not None:
            result["is_self_scale_item"] = from_union(
                [from_bool, from_none], self.is_self_scale_item)
        if self.assortment_code is not None:
            result["assortment_code"] = from_union(
                [from_int, from_none], self.assortment_code)
        if self.assortment_disclaimer is not None:
            result["assortment_disclaimer"] = from_union(
                [from_none, from_str], self.assortment_disclaimer)
        if self.assortment_label is not None:
            result["assortment_label"] = from_union(
                [from_none, from_str], self.assortment_label)
        if self.extra is not None:
            result["extra"] = from_union(
                [lambda x: to_class(Extra, x), from_none], self.extra)
        if self.warnings is not None:
            result["warnings"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.warnings)
        if self.department_id is not None:
            result["department_id"] = from_union(
                [from_int, from_none], self.department_id)
        if self.department_name is not None:
            result["department_name"] = from_union(
                [lambda x: to_enum(DepartmentName, x), from_none], self.department_name)
        if self.category_id is not None:
            result["category_id"] = from_union(
                [from_int, from_none], self.category_id)
        if self.category_name is not None:
            result["category_name"] = from_union(
                [lambda x: to_enum(CategoryNameEnum, x), from_none], self.category_name)
        if self.modified_at is not None:
            result["modified_at"] = from_union(
                [from_int, from_none], self.modified_at)
        if self.highlight_result is not None:
            result["_highlightResult"] = from_union(
                [lambda x: to_class(HighlightResult, x), from_none], self.highlight_result)
        return result


@dataclass
class Format:
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Format':
        assert isinstance(obj, dict)
        total = from_union([from_int, from_none], obj.get("total"))
        return Format(total)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.total is not None:
            result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class AfterFetch:
    format: Optional[Format] = None
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AfterFetch':
        assert isinstance(obj, dict)
        format = from_union([Format.from_dict, from_none], obj.get("format"))
        total = from_union([from_int, from_none], obj.get("total"))
        return AfterFetch(format, total)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.format is not None:
            result["format"] = from_union(
                [lambda x: to_class(Format, x), from_none], self.format)
        if self.total is not None:
            result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class GetIdx:
    load: Optional[Format] = None
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GetIdx':
        assert isinstance(obj, dict)
        load = from_union([Format.from_dict, from_none], obj.get("load"))
        total = from_union([from_int, from_none], obj.get("total"))
        return GetIdx(load, total)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.load is not None:
            result["load"] = from_union(
                [lambda x: to_class(Format, x), from_none], self.load)
        if self.total is not None:
            result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class Request:
    round_trip: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Request':
        assert isinstance(obj, dict)
        round_trip = from_union([from_int, from_none], obj.get("roundTrip"))
        return Request(round_trip)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.round_trip is not None:
            result["roundTrip"] = from_union(
                [from_int, from_none], self.round_trip)
        return result


@dataclass
class ProcessingTimingsMS:
    after_fetch: Optional[AfterFetch] = None
    get_idx: Optional[GetIdx] = None
    request: Optional[Request] = None
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ProcessingTimingsMS':
        assert isinstance(obj, dict)
        after_fetch = from_union(
            [AfterFetch.from_dict, from_none], obj.get("afterFetch"))
        get_idx = from_union([GetIdx.from_dict, from_none], obj.get("getIdx"))
        request = from_union(
            [Request.from_dict, from_none], obj.get("request"))
        total = from_union([from_int, from_none], obj.get("total"))
        return ProcessingTimingsMS(after_fetch, get_idx, request, total)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.after_fetch is not None:
            result["afterFetch"] = from_union(
                [lambda x: to_class(AfterFetch, x), from_none], self.after_fetch)
        if self.get_idx is not None:
            result["getIdx"] = from_union(
                [lambda x: to_class(GetIdx, x), from_none], self.get_idx)
        if self.request is not None:
            result["request"] = from_union(
                [lambda x: to_class(Request, x), from_none], self.request)
        if self.total is not None:
            result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class RenderingContent:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'RenderingContent':
        assert isinstance(obj, dict)
        return RenderingContent()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class CategoryDto:
    hits: Optional[List[Hit]] = None
    nb_hits: Optional[int] = None
    page: Optional[int] = None
    nb_pages: Optional[int] = None
    hits_per_page: Optional[int] = None
    facets: Optional[Facets] = None
    exhaustive_facets_count: Optional[bool] = None
    exhaustive_nb_hits: Optional[bool] = None
    exhaustive_typo: Optional[bool] = None
    exhaustive: Optional[Exhaustive] = None
    query: Optional[str] = None
    params: Optional[str] = None
    rendering_content: Optional[RenderingContent] = None
    processing_time_ms: Optional[int] = None
    processing_timings_ms: Optional[ProcessingTimingsMS] = None
    server_time_ms: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryDto':
        assert isinstance(obj, dict)
        hits = from_union([lambda x: from_list(lambda x:
                                               Hit.from_dict, x), from_none], obj.get("hits"))
        nb_hits = from_union([from_int, from_none], obj.get("nbHits"))
        page = from_union([from_int, from_none], obj.get("page"))
        nb_pages = from_union([from_int, from_none], obj.get("nbPages"))
        hits_per_page = from_union(
            [from_int, from_none], obj.get("hitsPerPage"))
        facets = from_union([Facets.from_dict, from_none], obj.get("facets"))
        exhaustive_facets_count = from_union(
            [from_bool, from_none], obj.get("exhaustiveFacetsCount"))
        exhaustive_nb_hits = from_union(
            [from_bool, from_none], obj.get("exhaustiveNbHits"))
        exhaustive_typo = from_union(
            [from_bool, from_none], obj.get("exhaustiveTypo"))
        exhaustive = from_union(
            [Exhaustive.from_dict, from_none], obj.get("exhaustive"))
        query = from_union([from_str, from_none], obj.get("query"))
        params = from_union([from_str, from_none], obj.get("params"))
        rendering_content = from_union(
            [RenderingContent.from_dict, from_none], obj.get("renderingContent"))
        processing_time_ms = from_union(
            [from_int, from_none], obj.get("processingTimeMS"))
        processing_timings_ms = from_union(
            [ProcessingTimingsMS.from_dict, from_none], obj.get("processingTimingsMS"))
        server_time_ms = from_union(
            [from_int, from_none], obj.get("serverTimeMS"))
        return CategoryDto(hits, nb_hits, page, nb_pages, hits_per_page, facets, exhaustive_facets_count, exhaustive_nb_hits, exhaustive_typo, exhaustive, query, params, rendering_content, processing_time_ms, processing_timings_ms, server_time_ms)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.hits is not None:
            result["hits"] = from_union([lambda x: from_list(
                lambda x: to_class(Hit, x), x), from_none], self.hits)
        if self.nb_hits is not None:
            result["nbHits"] = from_union([from_int, from_none], self.nb_hits)
        if self.page is not None:
            result["page"] = from_union([from_int, from_none], self.page)
        if self.nb_pages is not None:
            result["nbPages"] = from_union(
                [from_int, from_none], self.nb_pages)
        if self.hits_per_page is not None:
            result["hitsPerPage"] = from_union(
                [from_int, from_none], self.hits_per_page)
        if self.facets is not None:
            result["facets"] = from_union(
                [lambda x: to_class(Facets, x), from_none], self.facets)
        if self.exhaustive_facets_count is not None:
            result["exhaustiveFacetsCount"] = from_union(
                [from_bool, from_none], self.exhaustive_facets_count)
        if self.exhaustive_nb_hits is not None:
            result["exhaustiveNbHits"] = from_union(
                [from_bool, from_none], self.exhaustive_nb_hits)
        if self.exhaustive_typo is not None:
            result["exhaustiveTypo"] = from_union(
                [from_bool, from_none], self.exhaustive_typo)
        if self.exhaustive is not None:
            result["exhaustive"] = from_union(
                [lambda x: to_class(Exhaustive, x), from_none], self.exhaustive)
        if self.query is not None:
            result["query"] = from_union([from_str, from_none], self.query)
        if self.params is not None:
            result["params"] = from_union([from_str, from_none], self.params)
        if self.rendering_content is not None:
            result["renderingContent"] = from_union(
                [lambda x: to_class(RenderingContent, x), from_none], self.rendering_content)
        if self.processing_time_ms is not None:
            result["processingTimeMS"] = from_union(
                [from_int, from_none], self.processing_time_ms)
        if self.processing_timings_ms is not None:
            result["processingTimingsMS"] = from_union([lambda x: to_class(
                ProcessingTimingsMS, x), from_none], self.processing_timings_ms)
        if self.server_time_ms is not None:
            result["serverTimeMS"] = from_union(
                [from_int, from_none], self.server_time_ms)
        return result


def category_dto_from_dict(s: Any) -> CategoryDto:
    return CategoryDto.from_dict(s)


def category_dto_to_dict(x: CategoryDto) -> Any:
    return to_class(CategoryDto, x)
