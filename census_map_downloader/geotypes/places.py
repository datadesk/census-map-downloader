#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StatePlacesDownloader2018(BaseStateDownloader):
    """
    Download 2018 places for a single state.
    """
    YEAR = 2018
    PROCESSED_NAME = f"places_{YEAR}"
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
        return f"https://www2.census.gov/geo/tiger/TIGER{self.YEAR}/PLACE/tl_{self.YEAR}_{self.state.fips}_place.zip"

    @property
    def zip_name(self):
        return f"tl_{self.YEAR}_{self.state.fips}_place.zip"


class PlacesDownloader2018(BaseStateListDownloader):
    """
    Download all 2018 places in the United States.
    """
    YEAR = 2018
    PROCESSED_NAME = f"places_{YEAR}"
    DOWNLOADER_CLASS = StatePlacesDownloader2018
