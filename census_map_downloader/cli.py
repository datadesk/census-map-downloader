#! /usr/bin/env python
"""
Command-line interface.
"""
import click

import census_map_downloader


@click.group(help="Easily download U.S. census maps")
@click.option(
    "--data-dir",
    nargs=1,
    default="./",
    help="The folder where you want to download the data",
)
@click.option(
    "--year",
    default=None,
    type=int,
    help="The vintage of data to download. By default it gets the latest year. Not all data are available for every year.",
)
@click.pass_context
def cmd(ctx, data_dir="./", year=None):
    ctx.ensure_object(dict)
    ctx.obj["data_dir"] = data_dir
    ctx.obj["year"] = year


@cmd.command(help="Download places")
@click.pass_context
def places(ctx):
    obj = census_map_downloader.PlacesDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download tracts")
@click.pass_context
def tracts(ctx):
    obj = census_map_downloader.TractsDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download counties")
@click.pass_context
def counties(ctx):
    obj = census_map_downloader.CountiesDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download cartographic counties")
@click.pass_context
def counties_carto(ctx):
    obj = census_map_downloader.CountiesCartoDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download cartographic congressional districts")
@click.pass_context
def congress_carto(ctx):
    obj = census_map_downloader.CongressCartoDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download cartographic states")
@click.pass_context
def states_carto(ctx):
    obj = census_map_downloader.StatesCartoDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download cartographic state legislative districts(lower)")
@click.pass_context
def legislative_lower_carto(ctx):
    obj = census_map_downloader.LegislativeDistrictLowerCartoDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download cartographic state legislative districts(upper)")
@click.pass_context
def legislative_upper_carto(ctx):
    obj = census_map_downloader.LegislativeDistrictUpperCartoDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download cartographic county subdivisions")
@click.pass_context
def countysubdivision(ctx):
    obj = census_map_downloader.CountySubdivisionCartoDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download ZCTAs")
@click.pass_context
def zctas(ctx):
    obj = census_map_downloader.ZctasDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


@cmd.command(help="Download blocks")
@click.pass_context
def blocks(ctx):
    obj = census_map_downloader.BlocksDownloader(
        data_dir=ctx.obj["data_dir"], year=ctx.obj["year"]
    )
    obj.run()


if __name__ == "__main__":
    cmd()
