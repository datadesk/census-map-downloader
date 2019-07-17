#! /usr/bin/env python
# -*- coding: utf-8 -*-
import us
import geopandas as gpd
from census_map_downloader.base import BaseDownloader

# Logging
import logging
logger = logging.getLogger(__name__)


class StateTractsDownloader2010(BaseDownloader):
    """
    Download 2010 tracts for a single state.
    """
    def __init__(self, state, data_dir):
        # Configure the state
        self.state = us.states.lookup(state)
        super().__init__(data_dir)

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
    @property
    def url(self):
        return f"https://www2.census.gov/geo/tiger/TIGER2009/{self.zip_folder}/{self.zip_name}"

    @property
    def zip_name(self):
        return f"tl_2009_{self.state.fips}_tract00.zip"

    @property
    def zip_folder(self):
        return f"{self.state.fips}_{self.state.name.upper().replace(' ', '_')}"


class TractsDownloader2010(BaseDownloader):
    """
    Download all 2010 tracts in the United States.
    """
    PROCESSED_NAME = "tracts_2010"

    def run(self):
        self.download()
        self.process()

    def download(self):
        # Loop through all the states and download the shapes
        path_list = []
        for state in us.STATES:
            logger.debug(f"Downloading {state}")
            shp_path = StateTractsDownloader2010(
                state.abbr,
                data_dir=self.data_dir
            ).run()
            path_list.append(shp_path)

        # Open all the shapes
        df_list = [gpd.read_file(p) for p in path_list]

        # Concatenate them together
        df = gpd.pd.concat(df_list)

        # Write it out, if it doesn't already exist.
        us_path = self.data_dir.joinpath("us.shp")
        if us_path.exists():
            logger.debug(f"File already exists at {us_path}")
            return us_path
        logger.debug(f"Writing file with {len(df)} tracts to {us_path}")
        df.to_file(us_path, index=False)
        return us_path
