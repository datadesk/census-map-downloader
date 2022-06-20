#! /usr/bin/env python
import collections

# Logging
import logging

from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

logger = logging.getLogger(__name__)


class StateCountySubdivisionCartoDownloader(BaseStateDownloader):
    """
    Download cartographic county subdivisions for a single state.
    """

    YEAR_LIST = [2018]
    PROCESSED_NAME = "county_subdivision_carto"
    # Docs (https://www2.census.gov/geo/tiger/GENZ2018/2018_file_name_def.pdf?#)
    FIELD_CROSSWALK = collections.OrderedDict(
        {
            "STATEFP": "state_fips",
            "COUNTYFP": "county_fips",
            "COUSUBFP": "county_subdivision_fips",
            "GEOID": "geoid",
            "NAME": "name",
            "geometry": "geometry",
            "ALAND": "land_area",
            "AWATER": "water_area",
        }
    )

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ{self.year}/shp/cb_{self.year}_{self.state.fips}_cousub_500k.zip"

    @property
    def zip_name(self):
        return f"cb_{self.year}_{self.state.fips}_cousub_500k.zip"


class CountySubdivisionCartoDownloader(BaseStateListDownloader):
    """
    Download all cartographic county subdivisions in the United States.
    """

    YEAR_LIST = [2018]
    DOWNLOADER_CLASS = StateCountySubdivisionCartoDownloader

    def merge(self):
        """
        No merging on this downloader because it is too big.
        """
        pass

    def process(self):
        """
        No processing on this downloader because it is too big.
        """
        pass
