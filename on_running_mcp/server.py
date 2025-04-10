"""An MCP server for the On Running website."""

from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import requests
from io import BytesIO
from core.api import OnRunningAPI, Params
from core.schemas import (
    ProductSubType,
    ProductType,
    Payload,
    Request,
    Item,
    Filters,
    ShopFor,
)
from pydantic import Field


mcp = FastMCP("on_running_mcp", dependencies=["requests", "P"])


SESSION_STATE = {}


@mcp.tool(description="Make a query to the On Running API.")
def make_query(
    gender_filter: ShopFor | None = Field(description="The gender to shop for.", default=None),
    product_type: ProductType | None = Field(description="The type of product.", default=None),
    product_subtype: ProductSubType | None = Field(
        description="The subtype of the product.", default=None
    ),
) -> None:
    """Make a query to the On Running API."""
    filters = Filters(
        gender_filter=gender_filter,
        product_type=product_type,
        product_subtype=product_subtype,
    )
    params = Params(filters=filters)
    payload = OnRunningAPI(payload=Payload(requests=[Request(params=str(params))]))
    SESSION_STATE["payload"] = payload


@mcp.tool(description="Get product names from the On Running website.")
def get_product_names() -> list[str]:
    """Get product names from the On Running website."""
    if "payload" not in SESSION_STATE:
        raise ValueError("Please make a query first.")
    return SESSION_STATE["payload"].get_product_names()


@mcp.tool(description="Get activity and name key-value pairs.")
def get_activities() -> dict[str, str]:
    """Get activity and name key-value pairs."""
    if "payload" not in SESSION_STATE:
        raise ValueError("Please make a query first.")
    return SESSION_STATE["payload"].get_activities()


@mcp.tool(description="Filter by product name.")
def filter_by_product_name(
    product_name: str = Field(description="Product name"),
) -> Item | None:
    """Filter by product name."""
    if "payload" not in SESSION_STATE:
        raise ValueError("Please make a query first.")
    return SESSION_STATE["payload"].filter_by_product_name(name=product_name)


@mcp.tool(description="Get product image.")
def get_product_image(product_name: str = Field(description="Product name")):
    product = filter_by_product_name(product_name=product_name)
    response = requests.get(product.image_url)
    img = PILImage.open(BytesIO(response.content))
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")


@mcp.tool(description="Get product type options.")
def get_product_type_options() -> list[str]:
    """Get product type options."""
    return list(ProductType)


@mcp.tool(description="Get product subtype options.")
def get_product_subtype_options() -> list[str]:
    """Get product type options."""
    return list(ProductSubType)


@mcp.tool(description="Get gender options.")
def get_gender_options() -> list[str]:
    """Get product type options."""
    return list(ShopFor)
