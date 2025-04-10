from unittest import TestCase

from on_running_mcp.core.api import OnRunningAPI, Params
from on_running_mcp.core.schemas import Payload, ProductType, Request, Filters, ProductSubType, ShopFor


class TestAPI(TestCase):

    def test_create_api_instance(self):
        """Create an instance of OnRunningAPI."""
        filters = Filters(
            gender_filter=ShopFor.MEN,
            product_type=ProductType.ACCESSORIES,
            product_subtype=ProductSubType.SOCKS
        )
        params = Params(filters=filters)
        payload = Payload(requests=[Request(params=str(params))])
        api = OnRunningAPI(payload=payload)
        self.assertTrue(isinstance(api.hits, list))
