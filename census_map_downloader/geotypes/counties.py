#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class CountiesDownloader2018(BaseDownloader):
    """
    Download counties.
    """
    PROCESSED_NAME = "counties_2018"
    # Docs pg 21 (https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2018/TGRSHP2018_TechDoc_Ch3.pdf)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP": "state_fips",
        "COUNTYFP": "county_fips",
        "GEOID": "geoid",
        "NAME": "county_name",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return "https://www2.census.gov/geo/tiger/TIGER2018/COUNTY/tl_2018_us_county.zip"

    @property
    def zip_name(self):
        return f"tl_2018_us_county.zip"
