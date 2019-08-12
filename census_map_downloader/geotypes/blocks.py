#! /usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from census_map_downloader.base import BaseStateDownloader, BaseStateListDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateBlocksDownloader2018(BaseStateDownloader):
    """
    Download 2018 blocks for a single state.
    """
    YEAR = 2018
    PROCESSED_NAME = f"blocks_{YEAR}"
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
        return f"https://www2.census.gov/geo/tiger/TIGER{self.YEAR}/TABBLOCK/tl_{self.YEAR}_{self.state.fips}_tabblock10.zip"

    @property
    def zip_name(self):
        return f"tl_{self.YEAR}_{self.state.fips}_tabblock10.zip"


class BlocksDownloader2018(BaseStateListDownloader):
    """
    Download all 2018 blocks in the United States.
    """
    DOWNLOADER_CLASS = StateBlocksDownloader2018

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
