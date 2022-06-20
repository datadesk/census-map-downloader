#! /usr/bin/env python
# Logging
import logging
import pathlib
import time
import zipfile
from urllib.request import urlretrieve

import geopandas as gpd
import us

logger = logging.getLogger(__name__)


class BaseDownloader:
    YEAR_LIST = [2018]
    THIS_DIR = pathlib.Path(__file__).parent
    PARENT_DIR = THIS_DIR.parent

    def __init__(self, data_dir=None, year=None):
        # Set the download directory
        if data_dir:
            self.data_dir = pathlib.Path(str(data_dir))
        else:
            self.data_dir = self.PARENT_DIR.joinpath("data")

        if year is None:
            # If year is not specified, use the most recent year
            self.year = self.YEAR_LIST[-1]
        else:
            self.year = year

        # Validate the year
        if self.year not in self.YEAR_LIST:
            raise ValueError("This year is not supported for this geotype")

        # Initialize all the directories we will need
        if not self.data_dir.exists():
            self.data_dir.mkdir()
        self.raw_dir = self.data_dir.joinpath("raw")
        if not self.raw_dir.exists():
            self.raw_dir.mkdir()
        self.processed_dir = self.data_dir.joinpath("processed")
        if not self.processed_dir.exists():
            self.processed_dir.mkdir()

    def run(self):
        """
        Execute the downloader to fetch, prep and clean the source geotype files.
        """
        self.download()
        self.unzip()
        self.process()

    @property
    def zip_name(self):
        """
        The name of the source zipfile
        """
        raise NotImplementedError(
            "All geotype subclasses must provide their own zip_name property."
        )

    @property
    def zip_path(self):
        """
        The full path to the source zipfile.
        """
        return self.raw_dir.joinpath(self.zip_name)

    @property
    def shp_name(self):
        """
        The name of the source shapefile.
        """
        return self.zip_name.replace(".zip", ".shp")

    @property
    def shp_path(self):
        """
        The full path to the source shapefile.
        """
        return self.raw_dir.joinpath(self.shp_name)

    @property
    def geojson_name(self):
        """
        The name of the target GeoJSON created by this downloader.
        """
        return f"{self.PROCESSED_NAME}_{self.year}.geojson"

    @property
    def geojson_path(self):
        """
        The full path to the target GeoJSON created by this downloader.
        """
        return self.processed_dir.joinpath(self.geojson_name)

    def download(self):
        """
        Download the source geotype files.
        """
        # Check if the zip file already exists
        if self.zip_path.exists():
            logger.debug(f"ZIP file already exists at {self.zip_path}")
            return

        # If it doesn't, download it from the Census site
        logger.debug(f"Downloading {self.url} to {self.zip_path}")
        urlretrieve(self.url, self.zip_path)
        time.sleep(1)

    def unzip(self):
        """
        Unzip the source geotype files.
        """
        # Check if the shape has already been unzipped
        if self.shp_path.exists():
            logger.debug(f"SHP already unzipped at {self.shp_path}")
            return

        # If not, unzip it now.
        logger.debug(f"Unzipping {self.zip_path} to {self.raw_dir}")
        with zipfile.ZipFile(self.zip_path, "r") as z:
            z.extractall(self.raw_dir)

    def process(self):
        """
        Refine the source data and convert to cleaned GeoJSON.
        """
        # Check if the geojson file already exists
        if self.geojson_path.exists():
            logger.debug(f"GeoJSON file already exists at {self.geojson_path}")
            return

        # Read in the source shapefile
        gdf = gpd.read_file(self.shp_path)

        # Trim it down to the subset of fields we want to keep
        trimmed = gdf[list(self.FIELD_CROSSWALK.keys())]

        # Rename the fields using the crosswalk
        cleaned = trimmed.rename(columns=self.FIELD_CROSSWALK)

        # Write out a GeoJSON file
        logger.debug(f"Writing out {len(cleaned)} shapes to {self.geojson_path}")
        cleaned.to_file(self.geojson_path, driver="GeoJSON")


class BaseStateDownloader(BaseDownloader):
    """
    A base downloader for a single state's source files.
    """

    def __init__(self, state, data_dir, year):
        # Configure the state
        self.state = us.states.lookup(state)
        super().__init__(data_dir, year)

    @property
    def geojson_name(self):
        return f"{self.PROCESSED_NAME}_{self.year}_{self.state.abbr.lower()}.geojson"


class BaseStateListDownloader(BaseDownloader):
    """
    A base downloader that will retrieve all 50 states.
    """

    def run(self):
        self.download()
        self.merge()
        self.process()

    @property
    def merged_path(self):
        """
        The location of all the source shapefiles merged together.
        """
        return self.raw_dir.joinpath(f"{self.PROCESSED_NAME}_{self.year}.shp")

    def download(self):
        # Loop through all the states and download the shapes
        for state in us.STATES:
            logger.debug(f"Downloading {state}")
            try:
                runner = self.DOWNLOADER_CLASS(
                    state.abbr, data_dir=self.data_dir, year=self.year
                )
            except ValueError as e:
                # Creating the downloader class instance for the state raised
                # a `ValueError`. This is usually because the geotype isn't
                # supported for a particular state. For example, Nebraska
                # only has one chamber, so there's no file for the lower
                # cabinet.
                # Log this issue and keep going with the other states.
                logger.warning(e)
                continue

            runner.run()

    def merge(self):
        """
        Combine all the source shapefiles into a single shapefile.
        """
        if self.merged_path.exists():
            logger.debug(f"SHP file already exists at {self.merged_path}")
            return

        # Open all the shapes
        path_list = [
            self.DOWNLOADER_CLASS(
                state.abbr, data_dir=self.data_dir, year=self.year
            ).shp_path
            for state in us.STATES
        ]
        df_list = [gpd.read_file(p) for p in path_list]

        # Concatenate them together
        df = gpd.pd.concat(df_list)

        logger.debug(f"Writing file with {len(df)} tracts to {self.merged_path}")
        df.to_file(self.merged_path, index=False)

    def process(self):
        """
        Process the raw data and convert it to our preferred format, GeoJSON.
        """
        if self.geojson_path.exists():
            logger.debug(f"GeoJSON file already exists at {self.geojson_path}")
            return

        gdf = gpd.read_file(self.merged_path)
        logger.debug(f"Writing out {len(gdf)} shapes to {self.geojson_path}")
        gdf.to_file(self.geojson_path, driver="GeoJSON")
