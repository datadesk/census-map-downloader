#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import census_map_downloader


class CensusMapDownloadUnitTest(unittest.TestCase):

    def test_counties(self):
        census_map_downloader.CountiesDownloader2018().run()


if __name__ == '__main__':
    unittest.main()
