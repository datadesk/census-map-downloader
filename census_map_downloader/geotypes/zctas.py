#! /usr/bin/env python
# -*- coding: utf-8 -*-
import us
import collections
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
    YEAR = 2018
    # Docs pg 62 https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2018/TGRSHP2018_TechDoc_Ch3.pdf
    PROCESSED_NAME = f"zctas_{YEAR}"
    FIELD_CROSSWALK = collections.OrderedDict({
        "GEOID10": "geoid",
        "geometry": "geometry"
    })

    @property
    def url(self):
        return "https://www2.census.gov/geo/tiger/TIGER2018/ZCTA5/tl_2018_us_zcta510.zip"

    @property
    def zip_name(self):
        return f"tl_2018_us_zcta510.zip"

        # Add a raw download path for the relationships files
    @property
    def relationship_name(self):
        return "zcta_county_rel_10.txt"

    @property
    def relationship_path(self):
        return self.raw_dir.joinpath(self.relationship_name)

    def download(self):
        # Do the regular download
        super().download()

        # Also download the relationship file that connects ZCTAs to counties
        if self.relationship_path.exists():
            logger.debug(f"Relationship file already exists at {self.relationship_path}")
            return
        self.relationship_url = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
        logger.debug(f"Downloading {self.relationship_url} to {self.relationship_path}")
        urlretrieve(self.relationship_url, self.relationship_path)

    def process(self):
        """
        Refine the raw data and convert it to our preferred format, GeoJSON.
        """
        # Read in the raw shape
        gdf = gpd.read_file(self.shp_path)

        # Trim it down to the subset of fields we want to keep
        trimmed = gdf[list(self.FIELD_CROSSWALK.keys())]

        # Rename the fields using the crosswalk
        trimmed.rename(columns=self.FIELD_CROSSWALK, inplace=True)

        # Read relationship file
        df = pd.read_csv(
            self.relationship_path,
            usecols=['ZCTA5', 'STATE'],
            dtype={'ZCTA5': str, 'STATE': str}
        )

        # Loop through the 50 states
        for state in us.STATES:
            # Filter down to the ZCTAs in this state
            state_df = trimmed[trimmed.geoid.isin(df.loc[df.STATE == state.fips, 'ZCTA5'])]

            # Set page for this GeoJSON
            state_geojson_path = self.processed_dir.joinpath(f"{self.PROCESSED_NAME}_{state.abbr.lower()}.geojson")

            # Check if the geojson file already exists
            if state_geojson_path.exists():
                logger.debug(f"GeoJSON file already exists at {state_geojson_path}")
                continue

            # Write it out as GeoJSON
            logger.debug(f"Writing out {len(state_df)} shapes in {state} to {state_geojson_path}")
            state_df.to_file(state_geojson_path, driver="GeoJSON")
