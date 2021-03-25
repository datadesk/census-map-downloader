#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class CongressCartoDownloader(BaseDownloader):
    """
    Download cartographic congressional districts.
    """
    YEAR_LIST = [2018]
    PROCESSED_NAME = "congressionaldistricts_carto"
    # Docs (https://www2.census.gov/geo/tiger/GENZ2018/2018_file_name_def.pdf?#)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP": "state_fip",
        "CD116FP": "congresional_district",
        "GEOID": "geoid",
        "NAMELSAD": "name",
        "geometry": "geometry",
        "LSAD": "legal_statistical_area",
        "CDSESSN": "congressional_session_code",
        "ALAND": "land_area",
        "AWATER": "water_area"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ{self.year}/shp/cb_{self.year}_us_cd116_500k.zip"

    @property
    def zip_name(self):
        return f"cb_{self.year}_us_cd116_500k.zip"
