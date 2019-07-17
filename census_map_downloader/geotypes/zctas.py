#! /usr/bin/env python
# -*- coding: utf-8 -*-
import us
import pandas as pd
import geopandas as gpd
from urllib.request import urlretrieve
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

    def set_paths(self):
        # Set all the normals paths
        super().set_paths()

        # Add a raw download path for the relationships files
        self.relationship_name = "zcta_county_rel_10.txt"
        self.relationship_path = self.raw_dir.joinpath(self.relationship_name)

    def download(self):
        # Do the regular download
        super().download()

        # Also download the relationship file that connects ZCTAs to counties
        self.relationship_url = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
        logger.debug(f"Downloading {self.relationship_url} to {self.relationship_path}")
        urlretrieve(self.relationship_url, self.relationship_path)

    def process(self):
        """
        Refine the raw data and convert it to our preferred format, GeoJSON.
        """
        # Write out national file
        super().process()

        # Read in the raw shape
        gdf = gpd.read_file(self.shp_path)

        # Read relationship file
        df = pd.read_csv(
            self.relationship_path,
            usecols=['ZCTA5', 'STATE'],
            dtype={'ZCTA5': str, 'STATE': str}
        )

        # Loop through the 50 states
        for state in us.STATES:
            # Filter down to the ZCTAs in this state
            state_df = gdf[gdf.ZCTA5CE10.isin(df.loc[df.STATE == state.fips, 'ZCTA5'])]

            # Set page for this GeoJSON
            state_geojson_path = self.processed_dir.joinpath(f"2018_zctas_{state.abbr.lower()}.geojson")

            # Check if the geojson file already exists
            if state_geojson_path.exists():
                logger.debug(f"GeoJSON file already exists at {state_geojson_path}")
                return

            # Write it out as GeoJSON
            logger.debug(f"Writing out {len(state_df)} shapes in {state} to {state_geojson_path}")
            state_df.to_file(state_geojson_path, driver="GeoJSON")
