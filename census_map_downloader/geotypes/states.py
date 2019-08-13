#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StatesDownloader2018(BaseDownloader):
    """
    Download states.
    """
    YEAR = "2018"
    PROCESSED_NAME = f"states_{YEAR}"
    # Docs pg 53 (https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2018/TGRSHP2018_TechDoc_Ch3.pdf)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP": "state_fips",
        "GEOID": "geoid",
        "STUSPS": "state_abbr",
        "NAME": "state_name",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER{self.YEAR}/STATE/tl_{self.YEAR}_us_state.zip"

    @property
    def zip_name(self):
        return f"tl_{self.YEAR}_us_state.zip"
