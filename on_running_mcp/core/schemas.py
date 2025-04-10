"""Schemas for the On Running MCP server."""

from pydantic import BaseModel, Field
import datetime
from enum import StrEnum


class ShopFor(StrEnum):
    WOMEN = "womens"
    MEN = "mens"
    KIDS = "kids"


class ProductType(StrEnum):
    SHOES = "shoes"
    APPAREL = "apparel"
    ACCESSORIES = "accessories"


class ProductSubType(StrEnum):
    TOPS_AND_T_SHIRTS = "tops_and_t_shirts"
    SHORTS = "shorts"
    SOCKS = "socks"
    HOODIES_AND_SWEATSHIRTS = "hoodies_and_sweatshirts"
    PANTS = "pants"
    JACKETS = "jackets"
    TIGHTS = "tights"
    HEADWEAR = "headwear"
    BRAS = "bras"
    BAGS = "bags"
    SKIRTS_AND_DRESSES = "skirts_and_dresses"
    VESTS = "vests"
    SCARVES_AND_NECK_GAITERS = "scarves_and_neck_gaiters"
    ARM_SLEEVES = "arm_sleeves"
    LEG_WARMERS = "leg_warmers"


class Filters(BaseModel):
    gender_filter: ShopFor | None = Field(default=None)
    product_type: ProductType | None = Field(default=None)
    product_subtype: ProductSubType | None = Field(default=None)


class Store(BaseModel):
    price: float
    can_be_purchased: bool = Field(alias="canBePurchased")
    is_visible: bool = Field(alias="isVisible")
    is_hidden_from_search: bool = Field(alias="isHiddenFromSearch")
    discount_percentage: int = Field(alias="discountPercentage")
    purchasable_skus: list[str] = Field(alias="purchasableSkus")
    visible_skus: list[str] = Field(alias="visibleSkus")


class Item(BaseModel):
    name: str
    product_type: str | None = Field(alias="productType")
    product_subtype: str | None = Field(alias="productSubtype")
    product_subtype_style: list[str] = Field(alias="productSubtypeStyle")
    gender: str
    age_group: str | None = Field(alias="ageGroup")
    surface: str | None
    activities: list[str]
    available_from: datetime.datetime = Field(alias="availableFrom")
    collections: list[str]
    color_codes: list[str] = Field(alias="colorCodes")
    color_name: str = Field(alias="colorName")
    conditions: list[str]
    cushioning: str | None
    features: list[str]
    fit: str | None
    lacing: str | None
    family: str | None
    label: str | None
    road_running_style: str | None = Field(alias="roadRunningStyle")
    style_id: str = Field(alias="styleID")
    tags: list[str]
    technology: list[str]
    terrain: str | None
    vertical: str | None
    translated_fields: dict[str, dict[str, dict[str, str] | str | list[str]]] = Field(
        alias="translatedFields"
    )
    gender_filter: list[str] = Field(alias="genderFilter")
    image_url: str = Field(alias="imageUrl")
    grouping_key: str = Field(alias="groupingKey")
    grouping_key_v2: str = Field(alias="groupingKeyV2")
    products: list[dict]
    first_gallery_image_url: str = Field(alias="firstGalleryImageUrl")
    last_stock_synced: datetime.datetime = Field(alias="lastStockSynced")
    stock: int
    last_2_weeks_sales: int = Field(alias="last2WeeksSales")
    stores: dict[str, Store]
    sizes_apparel_men: list[str] | None = Field(alias="sizesApparelMen", default=None)
    last_1_week_sales_shoes_unbiased: int = Field(alias="last1WeekSalesShoesUnbiased")
    products_available_sizes: dict[str, dict[str, list[str]]] | None = Field(
        alias="productsAvailableSizes", default=None
    )
    marketing_image_url: str | None = Field(alias="marketingImageUrl")
    object_id: str = Field(alias="objectID")


class Request(BaseModel):
    indexName: str = Field(default="UK_products_production_v3")
    params: str


class Payload(BaseModel):
    requests: list[Request]
