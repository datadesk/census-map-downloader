#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateBlocksDownloader(BaseStateDownloader):
    """
    Download blocks for a single state.
    """
    YEAR_LIST = [2018]
    PROCESSED_NAME = "blocks"
    # Docs pg 14 (https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2018/TGRSHP2018_TechDoc_Ch3.pdf)
    FIELD_CROSSWALK = collections.OrderedDict({
        "STATEFP10": "state_fips",
        "COUNTYFP10": "county_fips",
        "BLOCKCE10": "block_id",
        "GEOID10": "geoid",
        "NAME10": "block_name",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER{self.year}/TABBLOCK/tl_{self.year}_{self.state.fips}_tabblock10.zip"

    @property
    def zip_name(self):
        return f"tl_{self.year}_{self.state.fips}_tabblock10.zip"


class BlocksDownloader(BaseStateListDownloader):
    """
    Download all blocks in the United States.
    """
    YEAR_LIST = [2018]
    DOWNLOADER_CLASS = StateBlocksDownloader

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
