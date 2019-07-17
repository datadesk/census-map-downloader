#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
    help="The folder where you want to download the data"
)
@click.pass_context
def cmd(ctx, data_dir="./"):
    ctx.ensure_object(dict)
    ctx.obj['data_dir'] = data_dir


@cmd.command(help="Download places")
@click.pass_context
def places(ctx):
    obj = census_map_downloader.PlacesDownloader2018()
    obj.run()


@cmd.command(help="Download tracts")
@click.pass_context
def tracts(ctx):
    obj = census_map_downloader.TractsDownloader2010()
    obj.run()


@cmd.command(help="Download counties")
@click.pass_context
def counties(ctx):
    obj = census_map_downloader.CountiesDownloader2018()
    obj.run()


@cmd.command(help="Download ZCTAs")
@click.pass_context
def zcta(ctx):
    obj = census_map_downloader.ZctasDownloader2018()
    obj.run()


if __name__ == '__main__':
    cmd()
