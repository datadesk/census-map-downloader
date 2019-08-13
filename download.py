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
    data_dir = "./"
    # census_map_downloader.BlocksDownloader2018(data_dir=data_dir).run()
    # census_map_downloader.TractsDownloader2010(data_dir=data_dir).run()
    census_map_downloader.CountiesDownloader2018(data_dir=data_dir).run()
    # census_map_downloader.PlacesDownloader2018(data_dir=data_dir).run()
    # census_map_downloader.ZctasDownloader2018(data_dir=data_dir).run()


if __name__ == '__main__':
    main()
