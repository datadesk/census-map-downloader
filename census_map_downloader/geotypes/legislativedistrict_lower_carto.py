#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateLegislativeDistrictLowerCartoDownloader(BaseStateDownloader):
    """
    Download cartographic state legislative districts (lower chamber) for a single state.
    """
    YEAR_LIST = [2018]
    PROCESSED_NAME = "legislative_district_lower_carto"
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

    def __init__(self, state, data_dir, year):
        if state == "NE":
            # Nebraska has a unicameral legislature
            raise ValueError(f"State {state} is not supported for this geotype")

        super().__init__(state, data_dir, year)

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ{self.year}/shp/cb_{self.year}_{self.state.fips}_sldl_500k.zip"

    @property
    def zip_name(self):
        return f"cb_{self.year}_{self.state.fips}_sldl_500k.zip"


class LegislativeDistrictLowerCartoDownloader(BaseStateListDownloader):
    """
    Download all cartographic state legislative districts (lower chamber) in the United States.
    """
    YEAR_LIST = [2018]
    DOWNLOADER_CLASS = StateLegislativeDistrictLowerCartoDownloader

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
