#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StatePlacesDownloader(BaseStateDownloader):
    """
    Download places for a single state.
    """
    YEAR_LIST = [2018]
    PROCESSED_NAME = "places"
    # Page 47 https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2018/TGRSHP2018_TechDoc_Ch3.pdf
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP": "state_fips",
        "PLACEFP": "place_id",
        "GEOID": "geoid",
        "NAME": "place_name",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER{self.year}/PLACE/tl_{self.year}_{self.state.fips}_place.zip"

    @property
    def zip_name(self):
        return f"tl_{self.year}_{self.state.fips}_place.zip"


class PlacesDownloader(BaseStateListDownloader):
    """
    Download all places in the United States.
    """
    YEAR_LIST = [2018]
    PROCESSED_NAME = "places"
    DOWNLOADER_CLASS = StatePlacesDownloader
