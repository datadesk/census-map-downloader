#! /usr/bin/env python
# -*- coding: utf-8 -*-
import us
import geopandas as gpd
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StatePlacesDownloader2018(BaseDownloader):
    """
    Download 2018 places for a single state.
    """
    YEAR = 2018

    def __init__(self, state, data_dir):
        # Configure the state
        self.state = us.states.lookup(state)
        super().__init__(data_dir)

    def set_paths(self):
        self.shp_name = self.zip_name.replace(".zip", ".shp")
        self.shp_path = self.raw_dir.joinpath(self.shp_name)
        self.zip_path = self.raw_dir.joinpath(self.zip_name)

    def run(self):
        self.download()
        self.unzip()
        return self.shp_path

    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER{self.YEAR}/PLACE/tl_{self.YEAR}_{self.state.fips}_place.zip"

    @property
    def zip_name(self):
        return f"tl_{self.YEAR}_{self.state.fips}_place.zip"


class PlacesDownloader2018(BaseDownloader):
    """
    Download all 2010 tracts in the United States.
    """
    YEAR = 2018
    PROCESSED_NAME = "places_2018"

    def __init__(self, data_dir=None):
        super().__init__(data_dir=data_dir)
        self.merged_path = self.raw_dir.joinpath("places_us_2018.shp")

    def run(self):
        self.download()
        self.process()

    def set_paths(self):
        self.geojson_name = f"{self.PROCESSED_NAME}.geojson"
        self.geojson_path = self.processed_dir.joinpath(self.geojson_name)

    def download(self):
        if self.merged_path.exists():
            logger.debug(f"SHP file already exists at {self.merged_path}")
            return

        # Loop through all the states and download the shapes
        path_list = []
        for state in us.STATES:
            logger.debug(f"Downloading {state}")
            shp_path = StatePlacesDownloader2018(
                state.abbr,
                data_dir=self.data_dir
            ).run()
            path_list.append(shp_path)

        # Open all the shapes
        df_list = [gpd.read_file(p) for p in path_list]

        # Concatenate them together
        df = gpd.pd.concat(df_list)

        logger.debug(f"Writing file with {len(df)} tracts to {self.merged_path}")
        df.to_file(self.merged_path, index=False)

    def process(self):
        """
        Refine the raw data and convert it to our preferred format, GeoJSON.
        """
        if self.geojson_path.exists():
            logger.debug(f"GeoJSON file already exists at {self.geojson_path}")
            return

        gdf = gpd.read_file(self.merged_path)
        logger.debug(f"Writing out {len(gdf)} shapes to {self.geojson_path}")
        gdf.to_file(self.geojson_path, driver="GeoJSON")
