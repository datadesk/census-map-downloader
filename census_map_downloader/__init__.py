#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Easily download U.S. census geographies
"""
import us
import time
import pathlib
import zipfile
import logging
import geopandas as gpd
from urllib.request import urlretrieve
logger = logging.getLogger(__name__)


class BaseDownloader(object):
    THIS_DIR = pathlib.Path(__file__).parent
    PARENT_DIR = THIS_DIR.parent

    def __init__(self, data_dir=None):
        # Set the download directory
        if data_dir:
            self.data_dir = pathlib.Path(str(data_dir))
        else:
            self.data_dir = self.PARENT_DIR.joinpath("data")
        if not self.data_dir.exists():
            self.data_dir.mkdir()

    def run(self):
        self.download()
        return self.unzip()

    def download(self):
        """
        Downloads the TIGER SHP file of Census block for the provided state and county.
        Returns the path to the ZIP file.
        """
        # Check if the zip file already exists
        zip_path = self.data_dir.joinpath(self.zip_name)
        if zip_path.exists():
            logger.debug(f"ZIP file already exists at {zip_path}")
            return zip_path

        # If it doesn't, download it from the Census FTP
        logger.debug(f"Downloading {self.url} to {zip_path}")
        urlretrieve(self.url, zip_path)
        time.sleep(1)

        # Return the path
        return zip_path

    def unzip(self):
        """
        Unzip the provided ZIP file.
        """
        # Check if the shape has already been unzipped
        shp_name = self.zip_name.replace(".zip", ".shp")
        shp_path = self.data_dir.joinpath(shp_name)
        if shp_path.exists():
            logger.debug(f"SHP already unzipped at {shp_path}")
            return shp_path

        # If not, unzip it now.
        zip_path = self.data_dir.joinpath(self.zip_name)
        logger.debug(f"Unzipping {zip_path} to {self.data_dir}")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(self.data_dir)

        # Pass back the shape path
        return shp_path


class CountyDownloader2018(BaseDownloader):
    """
    Download counties.
    """
    @property
    def url(self):
        return "https://www2.census.gov/geo/tiger/TIGER2018/COUNTY/tl_2018_us_county.zip"

    @property
    def zip_name(self):
        return f"tl_2018_us_county.zip"


class StateTractDownloader2010(BaseDownloader):
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


class StateTractDownloader2000(StateTractDownloader2010):
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


class USTractDownloader2010(BaseDownloader):
    """
    Download all 2010 tracts in the United States.
    """
    def run(self):
        # Loop through all the states and download the shapes
        path_list = []
        for state in us.STATES:
            logger.debug(f"Downloading {state}")
            shp_path = StateTractDownloader2010(
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
