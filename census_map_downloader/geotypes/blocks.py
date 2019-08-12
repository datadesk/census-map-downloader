#! /usr/bin/env python
# -*- coding: utf-8 -*-
import us
import collections
import geopandas as gpd
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateBlocksDownloader2018(BaseDownloader):
    """
    Download 2018 blocks for a single state.
    """
    YEAR = 2018
    PROCESSED_NAME = "blocks_2018"
    FIELD_CROSSWALK = collections.OrderedDict({
        "BLOCKCE10": "census_block",
        "GEOID10": "block_identifier",
        "NAME10": "census_block_name",
        "geometry": "geometry"
    })

    def __init__(self, state, data_dir):
        # Configure the state
        self.state = us.states.lookup(state)
        super().__init__(data_dir)

    def set_paths(self):
        self.shp_name = self.zip_name.replace(".zip", ".shp")
        self.shp_path = self.raw_dir.joinpath(self.shp_name)
        self.zip_path = self.raw_dir.joinpath(self.zip_name)
        self.geojson_name = f"{self.PROCESSED_NAME}_{self.state.abbr.upper()}.geojson"
        self.geojson_path = self.processed_dir.joinpath(self.geojson_name)

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER{self.YEAR}/TABBLOCK/tl_{self.YEAR}_{self.state.fips}_tabblock10.zip"

    @property
    def zip_name(self):
        return f"tl_{self.YEAR}_{self.state.fips}_tabblock10.zip"


class BlocksDownloader2018(BaseDownloader):
    """
    Download all 2018 blocks in the United States.
    """
    def run(self):
        self.download()

    def set_paths(self):
        pass

    def download(self):
        # Loop through all the states and download the shapes
        for state in us.STATES:
            print(f"Downloading {state}")
            shp_path = StateBlocksDownloader2018(
                state.abbr,
                data_dir=self.data_dir
            ).run()
