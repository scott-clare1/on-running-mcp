"""An on-running API."""

import requests
from .schemas import Payload, Item, Filters
from enum import StrEnum


URL = """https://algolia.on.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.24.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.77.0)%3B%20Vue%20(3.5.13)%3B%20Vue%20InstantSearch%20(4.20.1)%3B%20JS%20Helper%20(3.23.0)&x-algolia-api-key=bff229776989d153121333c90db826b1&x-algolia-application-id=ML35QLWPOC"""
HITS_PER_PAGE = 400


class FilterName(StrEnum):
    PRODUCT_TYPE = "productType"
    GENDER_FILTER = "genderFilter"
    PRODUCT_SUBTYPE = "productSubtype"


class Params:
    """Parameters for the API request."""

    def __init__(self, filters: Filters):
        self.filters = filters

    def _facet_filters(self) -> str:
        """Returns the facet filters for the API request."""
        query = "%5B"

        query_count = 0

        if self.filters.gender_filter:
            query += f"%5B%22{FilterName.GENDER_FILTER}%3A{self.filters.gender_filter.value}%22%5D"
            query_count += 1

        if self.filters.product_type:
            if query_count > 0:
                query += "%2C"

            query += f"%5B%22{FilterName.PRODUCT_TYPE}%3A{self.filters.product_type.value}%22%5D"
            query_count += 1

        if self.filters.product_subtype:
            if query_count > 0:
                query += "%2C"

            query += f"%5B%22{FilterName.PRODUCT_SUBTYPE}%3A{self.filters.product_subtype.value}%22%5D"
            query_count += 1

        query += "%5D"

        return query

    def __str__(self):
        params = (
            f"clickAnalytics=true&distinct=true&facetFilters={self._facet_filters()}&"
            "facets=%5B%22activities%22%2C%22collections%22%2C%22colorCodes%22%2C%22conditions%22%2C"
            "%22cushioning%22%2C%22family%22%2C%22features%22%2C%22fit%22%2C%22genderFilter%22%2C%"
            "22lacing%22%2C%22productSubtype%22%2C%22productSubtypeStyle%22%2C%22productType%22%2C%"
            "22roadRunningStyle%22%2C%22sizesApparelMen%22%2C%22sizesApparelWomen%22%2C%"
            "22sizesShoesKids%22%2C%22sizesShoesMen%22%2C%22sizesShoesWomen%22%2C%22surface%22%2C%"
            "22tags%22%2C%22technology%22%2C%22terrain%22%5D&filters=NOT%20productUrl%3ANULL%20AND%"
            "20NOT%20imageUrl%3ANULL%20AND%20NOT%20groupingKey%3ANULL%20AND%20stores.gb.isVisible%"
            "3Atrue%20AND%20stores.gb.isHiddenFromSearch%3Afalse%20AND%20NOT%20tags%"
            "3Aexclude_from_plp%20AND%20NOT%20tags%3Aclassics%20AND%20NOT%20tags%"
            f"3Alost_and_found&hitsPerPage={HITS_PER_PAGE}&maxValuesPerFacet=50&userToken=xxxxxxxx"
        )
        return params


class OnRunningAPI:

    def __init__(self, payload: Payload):
        self.payload = payload
        self.url = URL

        self.data = requests.post(self.url, json=self.payload.model_dump()).json()
        self.hits = self._validate_hits()

        if not self.hits:
            raise ValueError("No results found. Please try another search.")

    def _validate_hits(self) -> list[Item]:
        return [Item.model_validate(hit) for hit in self.data["results"][0]["hits"]]

    def get_product_names(self) -> list[str]:
        """Returns the product names from the API response."""

        return [hit.name for hit in self.hits]

    def get_activities(self) -> dict[str, list[str]]:
        """Returns the activities from the API response."""

        return {hit.name: hit.activities for hit in self.hits}

    def filter_by_product_name(self, name: str) -> Item | None:
        """Returns the product with the given name."""

        for hit in self.hits:
            if hit.name == name:
                return hit
        return None
