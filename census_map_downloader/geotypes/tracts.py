#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateTractsDownloader2010(BaseStateDownloader):
    """
    Download 2010 tracts for a single state.
    """
    YEAR_LIST = [2010]
    PROCESSED_NAME = "tracts"
    # Docs pg 57 (https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2018/TGRSHP2018_TechDoc_Ch3.pdf)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP10": "state_fips",
        "COUNTYFP10": "county_fips",
        "TRACTCE10": "tract_id",
        "GEOID10": "geoid",
        "NAME10": "tract_name",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return self.state.shapefile_urls("tract")

    @property
    def zip_name(self):
        return f"tl_2010_{self.state.fips}_tract10.zip"


class StateTractsDownloader2000(StateTractsDownloader2010):
    """
    Download 2000 tracts for a single state.
    """
    YEAR_LIST = [2000]
    # Docs pg 57 (https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2010/TGRSHP10SF1.pdf)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP00": "state_fips",
        "COUNTYFP00": "county_fips",
        "TRACTCE00": "tract_id",
        "CTIDFP00": "geoid",
        "NAME10": "tract_name",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER2009/{self.zip_folder}/{self.zip_name}"

    @property
    def zip_name(self):
        return f"tl_2009_{self.state.fips}_tract00.zip"

    @property
    def zip_folder(self):
        return f"{self.state.fips}_{self.state.name.upper().replace(' ', '_')}"

    @property
    def geojson_name(self):
        return f"{self.PROCESSED_NAME}_{self.year}_{self.state.abbr.lower()}.geojson"


class TractsDownloader(BaseStateListDownloader):
    """
    Download all 2000 tracts in the United States.
    """
    YEAR_LIST = [2000, 2010]
    PROCESSED_NAME = f"tracts"

    def __init__(self, data_dir=None, year=None):
        # Delegate to separate classes depending on the year
        # This approach avoids branching inside the property methods
        if year == 2000:
            self.DOWNLOADER_CLASS = StateTractsDownloader2000
        else:
            self.DOWNLOADER_CLASS = StateTractsDownloader2010

        super().__init__(data_dir, year)
