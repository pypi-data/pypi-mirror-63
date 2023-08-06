import json
import os

import click
from progress.bar import Bar

from sample_data_generator.core.connections import get_redis_connection
from sample_data_generator.core.sample_data_generator import SampleDataGenerator
from sample_data_generator.dao import SiteDaoRedis
from sample_data_generator.dao import SiteGeoDaoRedis
from sample_data_generator.schema import FlatSiteSchema

PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_SITES_FILENAME = os.path.join(PARENT_DIR, "sample_data_generator",
                                      "fixtures", "sites.json")


@click.command()
@click.option("-h",
              "--hostname",
              default="localhost",
              help="The hostname that Redis is running on")
@click.option("-p",
              "--port",
              default=6379,
              help="The port that Redis is running on")
@click.option(
    "-w",
    "--request-password",
    default=False,
    is_flag=True,
    help="Prompt interactively for the password to the Redis instance")
@click.option(
    "-f",
    "--filename",
    default=DEFAULT_SITES_FILENAME,
    help="The filename containing the JSON to load. If not specified, "
    "will load the sites.json file bundled with this application")
def load(hostname, port, request_password, filename):
    """Load the specified JSON file into Redis"""
    if request_password:
        password = input("Redis password: ")
        client = get_redis_connection(hostname, port, password)
    else:
        client = get_redis_connection(hostname, port)

    site_dao = SiteDaoRedis(client)
    site_geo_dao = SiteGeoDaoRedis(client)

    with open(filename, 'r') as f:
        sites = [FlatSiteSchema().load(d) for d in json.loads(f.read())]

    sample_generator = SampleDataGenerator(client, sites, days=1)

    sites_bar = Bar('Loading sites', max=len(sites))
    with client.pipeline(transaction=False) as p:
        for site in sites:
            sites_bar.next()
            site_dao.insert(site, pipeline=p)
            site_geo_dao.insert(site, pipeline=p)
        p.execute()

    print()
    readings_bar = Bar('Generating reading data', max=sample_generator.size)
    with client.pipeline(transaction=False) as p:
        for _ in sample_generator.generate(p):
            readings_bar.next()
        print("\nFinishing up...")
        p.execute()

    print("\nData load complete!")
