#! /usr/bin/env python
# -*- coding: utf-8 -*-
import us
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
        self.relationship_name = ""
        self.relationship_path = self.raw_dir.joinpath(self.relationship_name)

    def download(self):
        # Do the regular download
        super().download()
        # Also download the relationship file that connects ZCTAs to counties
        # If it doesn't, download it from the Census FTP
        relationship_url = ""
        logger.debug(f"Downloading {self.relationship_url} to {self.zip_path}")
        urlretrieve(relationship_url, self.relationship_path)

    def process(self):
        """
        Refine the raw data and convert it to our preferred format, GeoJSON.
        """
        # Write out SHP file
        gdf = gpd.read_file(self.shp_path)

        # Read in the relationship file
        df = pd.read_csv(self.relationship_path)

        # Merge the two
        merged = pd.merge()

        Check if the geojson file already exists
        if self.geojson_path.exists():
            logger.debug(f"GeoJSON file already exists at {self.geojson_path}")
        else:
            logger.debug(f"Writing out {len(gdf)} shapes to {self.geojson_path}")
            merged.to_file(self.geojson_path, driver="GeoJSON")

        # Loop through the 50 states and write out a GeoJSON for each
        for state in us.STATES:
            state_df = merged[merged.FIPS == state.fips]
            state_geojson_path = f""
            logger.debug(f"Writing out {len(state_df)} shapes in {{state}} to {state_geojson_path}")
            merged.to_file(state_geojson_path, driver="GeoJSON")
