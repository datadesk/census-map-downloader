#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class CountiesCartoDownloader(BaseDownloader):
    """
    Download cartographic counties.
    """
    YEAR_LIST = [2018]
    PROCESSED_NAME = "counties_carto"
    # Docs (https://www2.census.gov/geo/tiger/GENZ2018/2018_file_name_def.pdf?#)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP": "state_fips",
        "COUNTYFP": "county_fips",
        "GEOID": "geoid",
        "NAME": "county_name",
        "geometry": "geometry",
        "ALAND": "land_area",
        "AWATER": "water_area"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ{self.year}/shp/cb_{self.year}_us_county_500k.zip"

    @property
    def zip_name(self):
        return f"cb_{self.year}_us_county_500k.zip"
