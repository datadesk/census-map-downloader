#! /usr/bin/env python
# -*- coding: utf-8 -*-
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class CountiesDownloader2018(BaseDownloader):
    """
    Download counties.
    """
    PROCESSED_NAME = "counties_2018"

    @property
    def url(self):
        return "https://www2.census.gov/geo/tiger/TIGER2018/COUNTY/tl_2018_us_county.zip"

    @property
    def zip_name(self):
        return f"tl_2018_us_county.zip"
