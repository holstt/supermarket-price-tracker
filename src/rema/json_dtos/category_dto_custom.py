# type: ignore


from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

import dateutil.parser

# Not in use. Custom classes, not using optional for all fields.

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


# def to_class(c: Type[T], x: Any) -> dict:
#     assert isinstance(x, c)
#     return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]  # type: ignore


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_union(fs: list[Any], x: Any):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Exhaustive:
    facets_count: bool
    nb_hits: bool
    typo: bool

    @staticmethod
    def from_dict(obj: Any) -> "Exhaustive":
        assert isinstance(obj, dict)
        facets_count = from_bool(obj.get("facetsCount"))
        nb_hits = from_bool(obj.get("nbHits"))
        typo = from_bool(obj.get("typo"))
        return Exhaustive(facets_count, nb_hits, typo)


@dataclass
class Labels:
    rema1000: int
    eu_eco: int
    keyhole: int
    whole_grains: int

    @staticmethod
    def from_dict(obj: Any) -> "Labels":
        assert isinstance(obj, dict)
        rema1000 = from_int(obj.get("rema1000"))
        eu_eco = from_union([from_none, from_int], obj.get("eu_eco"))

        # eu_eco = from_int(obj.get("eu_eco"))
        keyhole = from_int(obj.get("keyhole"))
        whole_grains = from_int(obj.get("whole_grains"))
        return Labels(rema1000, eu_eco, keyhole, whole_grains)


@dataclass
class Facets:
    labels: Optional[Labels] = None

    @staticmethod
    def from_dict(obj: Any) -> "Facets":
        assert isinstance(obj, dict)
        labels = from_union([Labels.from_dict, from_none], obj.get("labels"))
        return Facets(labels)


@dataclass
class Extra:
    popularity: int
    video: None
    extended_description: None

    @staticmethod
    def from_dict(obj: Any) -> "Extra":
        assert isinstance(obj, dict)
        popularity = from_int(obj.get("popularity"))
        video = from_none(obj.get("video"))
        extended_description = from_none(obj.get("extended_description"))
        return Extra(popularity, video, extended_description)


class MatchLevel(Enum):
    NONE = "none"


@dataclass
class CategoryName:
    value: str
    match_level: MatchLevel
    matched_words: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> "CategoryName":
        assert isinstance(obj, dict)
        value = from_str(obj.get("value"))
        match_level = MatchLevel(obj.get("matchLevel"))
        matched_words = from_list(lambda x: x, obj.get("matchedWords"))
        return CategoryName(value, match_level, matched_words)


@dataclass
class HighlightResult:
    id: CategoryName
    name: CategoryName
    hf2: CategoryName
    labels: Optional[List[CategoryName]]
    search_words: List[CategoryName]
    category_name: CategoryName

    @staticmethod
    def from_dict(obj: Any) -> "HighlightResult":
        assert isinstance(obj, dict)
        id = CategoryName.from_dict(obj.get("id"))
        name = CategoryName.from_dict(obj.get("name"))
        hf2 = CategoryName.from_dict(obj.get("hf2"))
        labels = from_union(
            [lambda x: from_list(CategoryName.from_dict, x), from_none],
            obj.get("labels"),
        )
        search_words = from_union(
            [lambda x: from_list(CategoryName.from_dict, x), from_none],
            obj.get("search_words"),
        )
        category_name = CategoryName.from_dict(obj.get("category_name"))
        return HighlightResult(id, name, hf2, labels, search_words, category_name)


@dataclass
class NutritionInfo:
    name: str
    value: str
    sort: int

    @staticmethod
    def from_dict(obj: Any) -> "NutritionInfo":
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        value = from_str(obj.get("value"))
        sort = int(from_str(obj.get("sort")))
        return NutritionInfo(name, value, sort)


@dataclass
class Pricing:
    price: float
    max_quantity: int
    price_over_max: float
    is_on_discount: bool
    normal_price: float
    price_per_kilogram: float
    price_per_unit: str
    is_advertised: bool
    deposit: int
    price_changes_on: Optional[datetime] = None
    price_changes_type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Pricing":
        assert isinstance(obj, dict)
        price = from_float(obj.get("price"))
        max_quantity = from_int(obj.get("max_quantity"))
        price_over_max = from_float(obj.get("price_over_max"))
        is_on_discount = from_bool(obj.get("is_on_discount"))
        normal_price = from_float(obj.get("normal_price"))
        price_per_kilogram = from_float(obj.get("price_per_kilogram"))
        price_per_unit = from_str(obj.get("price_per_unit"))
        price_changes_on = from_union(
            [from_none, from_datetime], obj.get("price_changes_on")
        )
        price_changes_type = from_union(
            [from_none, from_str], obj.get("price_changes_type")
        )
        is_advertised = from_bool(obj.get("is_advertised"))
        deposit = from_int(obj.get("deposit"))
        return Pricing(
            price,
            max_quantity,
            price_over_max,
            is_on_discount,
            normal_price,
            price_per_kilogram,
            price_per_unit,
            is_advertised,
            deposit,
            price_changes_on,
            price_changes_type,
        )


@dataclass
class Hit:
    id: int
    name: str
    underline: str
    hf2: str
    country_of_origin_code: str
    pricing: Pricing
    labels: List[str]
    wine_type_labels: List[Any]
    season_labels: List[Any]
    review_labels: List[Any]
    fits_with_labels: List[Any]
    description: str
    description_short: str
    hp_statements: List[Any]
    declaration: str
    declaration_old: str
    nutrition_info: List[NutritionInfo]
    nutrition_info_old: List[Any]
    image_url: str
    have_image: bool
    bar_codes: List[str]
    search_words: List[str]
    min_age: None
    sorting: int
    is_weight_item: bool
    median_weight: int
    median_weight_unit: str
    is_self_scale_item: bool
    item_label: None
    item_disclaimer: None
    assortment_code: int
    extra: Extra
    temperature_zone: None
    warnings: List[Any]
    department_id: int
    department_name: str
    category_id: int
    category_name: str
    modified_at: int
    object_id: int
    highlight_result: HighlightResult
    assortment_disclaimer: Optional[str] = None
    assortment_label: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        underline = from_str(obj.get("underline"))
        hf2 = from_str(obj.get("hf2"))
        country_of_origin_code = from_str(obj.get("country_of_origin_code"))
        pricing = Pricing.from_dict(obj.get("pricing"))
        labels = from_list(from_str, obj.get("labels"))
        wine_type_labels = from_list(lambda x: x, obj.get("wine_type_labels"))
        season_labels = from_list(lambda x: x, obj.get("season_labels"))
        review_labels = from_list(lambda x: x, obj.get("review_labels"))
        fits_with_labels = from_list(lambda x: x, obj.get("fits_with_labels"))
        description = from_str(obj.get("description"))
        description_short = from_str(obj.get("description_short"))
        hp_statements = from_list(lambda x: x, obj.get("hp_statements"))
        declaration = from_str(obj.get("declaration"))
        declaration_old = from_str(obj.get("declaration_old"))
        nutrition_info = from_list(NutritionInfo.from_dict, obj.get("nutrition_info"))
        nutrition_info_old = from_list(lambda x: x, obj.get("nutrition_info_old"))
        image_url = from_str(obj.get("image_url"))
        have_image = from_bool(obj.get("have_image"))
        bar_codes = from_list(from_str, obj.get("bar_codes"))
        search_words = from_list(from_str, obj.get("search_words"))
        min_age = from_none(obj.get("min_age"))
        sorting = from_int(obj.get("sorting"))
        is_weight_item = from_bool(obj.get("is_weight_item"))
        median_weight = from_int(obj.get("median_weight"))
        median_weight_unit = from_str(obj.get("median_weight_unit"))
        is_self_scale_item = from_bool(obj.get("is_self_scale_item"))
        item_label = from_none(obj.get("item_label"))
        item_disclaimer = from_none(obj.get("item_disclaimer"))
        assortment_code = from_int(obj.get("assortment_code"))
        assortment_disclaimer = from_union(
            [from_none, from_str], obj.get("assortment_disclaimer")
        )
        assortment_label = from_union(
            [from_none, from_str], obj.get("assortment_label")
        )
        extra = Extra.from_dict(obj.get("extra"))
        temperature_zone = from_none(obj.get("temperature_zone"))
        warnings = from_list(lambda x: x, obj.get("warnings"))
        department_id = from_int(obj.get("department_id"))
        department_name = from_str(obj.get("department_name"))
        category_id = from_int(obj.get("category_id"))
        category_name = from_str(obj.get("category_name"))
        modified_at = from_int(obj.get("modified_at"))
        object_id = int(from_str(obj.get("objectID")))
        highlight_result = HighlightResult.from_dict(obj.get("_highlightResult"))
        return Hit(
            id,
            name,
            underline,
            hf2,
            country_of_origin_code,
            pricing,
            labels,
            wine_type_labels,
            season_labels,
            review_labels,
            fits_with_labels,
            description,
            description_short,
            hp_statements,
            declaration,
            declaration_old,
            nutrition_info,
            nutrition_info_old,
            image_url,
            have_image,
            bar_codes,
            search_words,
            min_age,
            sorting,
            is_weight_item,
            median_weight,
            median_weight_unit,
            is_self_scale_item,
            item_label,
            item_disclaimer,
            assortment_code,
            extra,
            temperature_zone,
            warnings,
            department_id,
            department_name,
            category_id,
            category_name,
            modified_at,
            object_id,
            highlight_result,
            assortment_disclaimer,
            assortment_label,
        )


@dataclass
class Request:
    round_trip: int

    @staticmethod
    def from_dict(obj: Any) -> "Request":
        assert isinstance(obj, dict)
        round_trip = from_int(obj.get("roundTrip"))
        return Request(round_trip)


@dataclass
class ProcessingTimingsMS:
    request: Request

    @staticmethod
    def from_dict(obj: Any) -> "ProcessingTimingsMS":
        assert isinstance(obj, dict)
        request = Request.from_dict(obj.get("request"))
        return ProcessingTimingsMS(request)


@dataclass
class RenderingContent:
    pass

    @staticmethod
    def from_dict(obj: Any) -> "RenderingContent":
        assert isinstance(obj, dict)
        return RenderingContent()


@dataclass
class CategoryDto:
    hits: List[Hit]
    nb_hits: int
    page: int
    nb_pages: int
    hits_per_page: int
    facets: Facets
    exhaustive_facets_count: bool
    exhaustive_nb_hits: bool
    exhaustive_typo: bool
    exhaustive: Exhaustive
    query: str
    params: str
    rendering_content: RenderingContent
    processing_time_ms: int
    processing_timings_ms: ProcessingTimingsMS

    @staticmethod
    def from_dict(obj: Any) -> "CategoryDto":
        assert isinstance(obj, dict)
        hits = from_list(Hit.from_dict, obj.get("hits"))
        nb_hits = from_int(obj.get("nbHits"))
        page = from_int(obj.get("page"))
        nb_pages = from_union([from_int, from_none], obj.get("nbPages"))
        hits_per_page = from_int(obj.get("hitsPerPage"))
        facets = from_union([Facets.from_dict, from_none], obj.get("facets"))
        exhaustive_facets_count = from_bool(obj.get("exhaustiveFacetsCount"))
        exhaustive_nb_hits = from_bool(obj.get("exhaustiveNbHits"))
        exhaustive_typo = from_bool(obj.get("exhaustiveTypo"))
        exhaustive = Exhaustive.from_dict(obj.get("exhaustive"))
        query = from_str(obj.get("query"))
        params = from_str(obj.get("params"))
        rendering_content = RenderingContent.from_dict(obj.get("renderingContent"))
        processing_time_ms = from_int(obj.get("processingTimeMS"))
        processing_timings_ms = ProcessingTimingsMS.from_dict(
            obj.get("processingTimingsMS")
        )
        return CategoryDto(
            hits,
            nb_hits,
            page,
            nb_pages,
            hits_per_page,
            facets,
            exhaustive_facets_count,
            exhaustive_nb_hits,
            exhaustive_typo,
            exhaustive,
            query,
            params,
            rendering_content,
            processing_time_ms,
            processing_timings_ms,
        )


def category_dto_from_dict(s: Any) -> CategoryDto:
    return CategoryDto.from_dict(s)
