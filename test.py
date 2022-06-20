#! /usr/bin/env python
import shutil
import unittest
from pathlib import Path

import census_map_downloader


class BaseDownloaderTestCase(unittest.TestCase):
    def test_init_unsupported_year(self):
        """Test that constructor raises an exception for an unsupported year"""

        with self.assertRaises(ValueError):
            census_map_downloader.BaseDownloader(year=1900)


class CountiesDownloaderTestCase(unittest.TestCase):
    def setUp(self):
        self.MOST_RECENT_YEAR = 2020
        self.DATA_DIR = Path(__file__).resolve().parent / "test-data"

        self.DATA_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        """Tear down test environment"""
        shutil.rmtree(self.DATA_DIR)

    def test_init_default_year(self):
        """
        Test that a default year attribute is set when no year is passed to
        constructor
        """
        downloader = census_map_downloader.CountiesDownloader()
        self.assertEqual(downloader.year, self.MOST_RECENT_YEAR)

    def test_init_specify_year(self):
        """
        Test that the year attribute is set to the year passed to the
        constructor
        """
        downloader = census_map_downloader.CountiesDownloader(year=2018)
        self.assertEqual(downloader.year, 2018)

    def test_url_default_year(self):
        """
        Test that the download URL reflects the default year when no year is
        passed to thee constructor
        """
        downloader = census_map_downloader.CountiesDownloader()
        self.assertTrue(str(self.MOST_RECENT_YEAR) in downloader.url)

    def test_url_specify_year(self):
        """
        Test that the download URL reflects the year passed to the constructor
        """
        downloader = census_map_downloader.CountiesDownloader(year=2018)
        self.assertTrue("2018" in downloader.url)

    def test_run_default_year(self):
        """
        Test that the default year's shapefile is downloaded and processed
        when no year is passed to the constructor
        """
        # TODO: This is more of an integration test because it makes a request
        # and touches the filesystem. It might be better to mock
        # various classes and methods to detect whether things like
        # urlretrive() are called. We don't need to test their
        # functionality.
        downloader = census_map_downloader.CountiesDownloader(data_dir=self.DATA_DIR)
        downloader.run()

        shapefile_zip_path = (
            self.DATA_DIR / "raw" / f"tl_{self.MOST_RECENT_YEAR}_us_county.zip"
        )
        self.assertTrue(shapefile_zip_path.is_file())
        shapefile_path = (
            self.DATA_DIR / "raw" / f"tl_{self.MOST_RECENT_YEAR}_us_county.shp"
        )
        self.assertTrue(shapefile_path.is_file())
        geojson_path = (
            self.DATA_DIR / "processed" / f"counties_{self.MOST_RECENT_YEAR}.geojson"
        )
        self.assertTrue(geojson_path.is_file())

    def test_run_specify_year(self):
        """
        Test that the shapefile that is downloaded and processed
        reflects the year passed to the constructor
        """
        # TODO: This is more of an integration test because it makes a request
        # and touches the filesystem. It might be better to mock
        # various classes and methods to detect whether things like
        # urlretrive() are called. We don't need to test their
        # functionality.
        year = 2018
        downloader = census_map_downloader.CountiesDownloader(
            data_dir=self.DATA_DIR, year=year
        )
        downloader.run()

        shapefile_zip_path = self.DATA_DIR / "raw" / f"tl_{year}_us_county.zip"
        self.assertTrue(shapefile_zip_path.is_file())
        shapefile_path = self.DATA_DIR / "raw" / f"tl_{year}_us_county.shp"
        self.assertTrue(shapefile_path.is_file())
        geojson_path = self.DATA_DIR / "processed" / f"counties_{year}.geojson"
        self.assertTrue(geojson_path.is_file())


if __name__ == "__main__":
    unittest.main()
