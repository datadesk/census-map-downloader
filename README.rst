census-map-downloader
=====================

Easily download U.S. census maps


Installation
------------

::

    $ pipenv install census-map-downloader


Command line usage
------------------

::

    Usage: censusmapdownloader [OPTIONS] COMMAND [ARGS]...

      Easily download U.S. census maps

    Options:
      --data-dir TEXT  The folder where you want to download the data
      --help           Show this message and exit.

    Commands:
    blocks                   Download blocks
    congress-carto           Download cartographic congressional districts
    counties                 Download counties
    counties-carto           Download cartographic counties
    countysubdivision        Download cartographic county subdivisions
    legislative-lower-carto  Download cartographic state legislative (lower chamber)
    legislative-upper-carto  Download cartographic state legislative (upper chamber)
    places                   Download places
    states-carto             Download cartographic states
    tracts                   Download tracts
    zctas                    Download ZCTAs

Examples
------------------

Here's an example of downloading all counties ::

    $ censusmapdownloader counties

You can specify the download directory with --data-dir ::

    $ censusmapdownloader --data-dir ./my-special-folder/ counties

Contributing
------------

Install dependencies for development ::

    $ pipenv install --dev

Run tests ::

    $ make test

Ship new version to PyPI ::

    $ make ship

Adding additional years to a dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Downloader classes for different geography types are defined in modules of :code:`census_map_downloader.geotypes`. For example, the downloader for countie is :code:`census_map_downloader.geotypes.counties.CountiesDownloader`.

If the URL and fields in a shapefile are the same as those for years that are already supported, you can just add the year to the :code:`YEAR_LIST` attribute.

If the fields are the same, but the URL changes between groups of years, add logic to the :code:`url` property method of the downloader classes to alter the URL based on :code:`self.year`.

If the fields and URL change from year to year, consider creating classes for each year and delegating to :code:`census_map_downloader.geotypes.tracts.TractsDownloader` is an example of a class that uses this approach.

Developing the CLI
------------------

The command-line interface is implemented using Click and setuptools. To install it locally for development inside your virtual environment, run the following installation command, as `prescribed by the Click documentation <https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration>`_. ::

    $ pip install --editable .
