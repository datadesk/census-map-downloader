#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateLegislativeDistrictUpperCartoDownloader2018(BaseStateDownloader):
    """
    Download 2018 cartographic state legislative districts (upper chamber) for a single state.
    """
    PROCESSED_NAME = "legislative_district_upper_carto_2018"
    # Docs (https://www2.census.gov/geo/tiger/GENZ2018/2018_file_name_def.pdf?#)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP": "state_fips",
        "GEOID": "geoid",
        "LSY": "legislative_session_year",
        "NAME": "name",
        "geometry": "geometry",
        "ALAND": "land_area",
        "AWATER": "water_area"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_{self.state.fips}_sldu_500k.zip"

    @property
    def zip_name(self):
        return f"cb_2018_{self.state.fips}_sldu_500k.zip"


class LegislativeDistrictUpperCartoDownloader2018(BaseStateListDownloader):
    """
    Download all 2018 cartographic state legislative districts (upper chamber) in the United States.
    """
    DOWNLOADER_CLASS = StateLegislativeDistrictUpperCartoDownloader2018

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
