"""
Download all the data.
"""
import logging
import census_map_downloader


def main():
    # Configure logging
    logger = logging.getLogger('census_map_downloader')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    census_map_downloader.BlocksDownloader2018().run()
    # census_map_downloader.USTractDownloader2010()
    # census_map_downloader.CountyDownloader2018().run()
    # census_map_downloader.ZctasDownloader2018().run()


if __name__ == '__main__':
    main()
