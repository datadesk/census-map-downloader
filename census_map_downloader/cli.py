#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Command-line interface.
"""
import click
import census_map_downloader


@click.group(help="Easily download U.S. census maps")
@click.pass_context
def cmd(ctx, data_dir="./"):
    ctx.ensure_object(dict)
    ctx.obj['data_dir'] = data_dir


@cmd.command(help="Download places")
@click.pass_context
def places(ctx):
    obj = census_map_downloader.USPlaceDownloader2018()
    obj.run()


@cmd.command(help="Download tracts")
@click.pass_context
def tracts(ctx):
    obj = census_map_downloader.USTractDownloader2010()
    obj.run()


@cmd.command(help="Download counties")
@click.pass_context
def counties(ctx):
    obj = census_map_downloader.CountyDownloader2018()
    obj.run()


if __name__ == '__main__':
    cmd()
