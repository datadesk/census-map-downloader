#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class LegislativeDistrictLowerCartoDownloader2018(BaseDownloader):
    """
    Download 2018 cartographic state legislative districts (lower chamber).
    """
    PROCESSED_NAME = "legislative_district_lower_carto_2018"
    # Docs (https://www2.census.gov/geo/tiger/GENZ2018/2018_file_name_def.pdf?#)
    FIELD_CROSSWALK = collections.OrderedDict({
		"STATEFP": "state_fips",
        "GEOID": "geoid",
        "SLDSLST": "current_state_legislative_district_lower_code",
        "LSY": "legislative_session_year",
        "NAME": "name",
        "geometry": "geometry",
        "ALAND": "land_area",
        "AWATER": "water_area"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_{self.state.fips}_sldl_500k.zip"

    @property
    def zip_name(self):
        return f"cb_2018_{self.state.fips}_sldl_500k.zip"

    @property
    def zip_folder(self):
        return f"{self.state.fips}_{self.state.name.upper().replace(' ', '_')}"

    @property
    def geojson_name(self):
        return f"{self.PROCESSED_NAME}_{self.state.abbr.lower()}.geojson"