import logging
import os
import datetime

import pandas as pd
import click

from auction.session.operators import Drouot, Interencheres

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


@click.group()
def cli():
    """Auction utils"""
    click.echo('Package Auction')


@cli.command()
@click.option('--item',
              "-i",
              default=False,
              help='Item to search')
def search(item):
    """Find object on Interencheres and Drouotlive

    Args:
        link (str): The link to the english webpage
    """

    # Get items from drouot website
    click.echo("Getting data from drouot ...")
    drouot = Drouot(item)
    df_drouot = drouot.transform()

    # Get items from interencheres
    click.echo("Getting data from interencheres ...")
    interencheres = Interencheres(item)
    df_interencheres = interencheres.transform()

    # Concat df & extract to csv
    df = pd.concat([df_drouot, df_interencheres])
    df.to_excel(
        f'auction_searchs_{datetime.datetime.now().date()}.xlsx',
        index=False)
