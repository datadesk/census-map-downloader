#! /usr/bin/env python
import collections

# Logging
import logging

from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

logger = logging.getLogger(__name__)


class StateLegislativeDistrictUpperCartoDownloader(BaseStateDownloader):
    """
    Download cartographic state legislative districts (upper chamber) for a single state.
    """

    YEAR_LIST = [2018]
    PROCESSED_NAME = "legislative_district_upper_carto"
    # Docs (https://www2.census.gov/geo/tiger/GENZ2018/2018_file_name_def.pdf?#)
    FIELD_CROSSWALK = collections.OrderedDict(
        {
            "STATEFP": "state_fips",
            "GEOID": "geoid",
            "LSY": "legislative_session_year",
            "NAME": "name",
            "geometry": "geometry",
            "ALAND": "land_area",
            "AWATER": "water_area",
        }
    )

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/GENZ{self.year}/shp/cb_{self.year}_{self.state.fips}_sldu_500k.zip"

    @property
    def zip_name(self):
        return f"cb_{self.year}_{self.state.fips}_sldu_500k.zip"


class LegislativeDistrictUpperCartoDownloader(BaseStateListDownloader):
    """
    Download all cartographic state legislative districts (upper chamber) in the United States.
    """

    YEAR_LIST = [2018]
    DOWNLOADER_CLASS = StateLegislativeDistrictUpperCartoDownloader

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
