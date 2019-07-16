#! /usr/bin/env python
# -*- coding: utf-8 -*-
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class ZctasDownloader2018(BaseDownloader):
    """
    Download 5-digit ZIP Code Tabulation Area
    """
    PROCESSED_NAME = "zctas_2018"

    @property
    def url(self):
        return "https://www2.census.gov/geo/tiger/TIGER2018/ZCTA5/tl_2018_us_zcta510.zip"

    @property
    def zip_name(self):
        return f"tl_2018_us_zcta510.zip"