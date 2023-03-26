import click
import pandas as pd
import requests
import csv

from dagster import MetadataValue, Output, asset, op, materialize, job
from urllib.parse import urlparse



@asset
def load_data():
    data = {'id': ['1', '2'], 'name': ['hello', 'world'], 'url': ['http://hello.com/home', 'https://world.org/']}
    # Create DataFrame
    df = pd.DataFrame(data)

    metadata = {
        "num_records": len(df),
        "preview": MetadataValue.md(df[["id", "name", "url"]].to_markdown()),
    }
    return df

@asset
def add_domain(load_data):
    load_data['domain_of_url'] = load_data['url']
    load_data['domain_of_url'] = load_data['domain_of_url'].apply((lambda x: urlparse(x).netloc))
    metadata = {
        "num_records": len(load_data),
        "preview": MetadataValue.md(load_data[["id", "name", "url"]].to_markdown()),
    }
    return Output(value=load_data, metadata=metadata)


@asset
def copy_to_file(add_domain,path_out):
    add_domain.to_csv(path_out)


def run_assets():
    materialize(assets=[load_data, add_domain, copy_to_file])
