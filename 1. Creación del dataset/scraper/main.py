import os

import click

from dbkpop.DBKpopManager import DBKpopManager
from gaon.GaonManager import GaonManager


@click.group()
def scraper():
    pass


@click.command('')
@click.option('--until', default=2009, help='Year to stop')
@click.option('--output', default=os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "data"), help='Output folder')
def gaon(until, output):
    """
    Get and save dataset with gaon monthly songs
    """
    print(f'Getting the chart songs until {until}')
    output = f"{output}/gaon_monthly_chart_until_{until}.csv"

    until = int(until)
    gaon_manager = GaonManager()
    gaon_manager.save_songs(output=output, until=until)


@click.command('')
@click.option('--output', default=os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "data"), help='Output folder')
def dbkpop(output):
    """
    Get and save DBKpop tables
    """
    print('Scraping and parsing the dbkpop data')
    dbkpop_manager = DBKpopManager(data_folder=output)
    print("Started scraping and parsing Kpop boybands")
    dbkpop_manager.save_k_pop_table("https://dbkpop.com/db/k-pop-boybands",
                                    "all_kpop_boybands.csv")
    print("Started scraping and parsing Kpop girlgroups")
    dbkpop_manager.save_k_pop_table("https://dbkpop.com/db/k-pop-girlgroups",
                                    "all_k_pop_girlgroups.csv")
    print("Started scraping and parsing Kpop idols")
    dbkpop_manager.save_k_pop_table("https://dbkpop.com/db/all-k-pop-idols",
                                    "all_k_pop_idols.csv")


scraper.add_command(gaon)
scraper.add_command(dbkpop)

if __name__ == '__main__':
    scraper()
