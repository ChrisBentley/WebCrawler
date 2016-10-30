#!/usr/bin/env python

"""
Program that accepts and url and creates a site map of of the domain.
Static Assets of each page are displayed.

Author: Chris Bentley
"""

import argparse
from urllib.request import urlopen
from urllib.parse import urlparse
from werkzeug import urls


def create_site_map(domain):
    """
    Method to create a site map for a given url
    :param domain: The domain to create a site map of
    :return: JSON object containing a site map of unique urls
    """
    site_map = {}

    print(domain)

    return site_map


def extract_static_assets(url):
    """
    Method to extract all the static assets for a given url
    :param url: The url containing the domain to create a site map of
    :return: Array containing a list of static assets
    """
    static_assets = []

    return static_assets


def make_url_safe(url):
    """
    Method to add a scheme if one is not provided
    and make sure the path is safe from error such as spaces
    :param url: The url to be made safe
    :return: A safe url as a string
    """
    if not urlparse(url).scheme:
       url = "http://" + url

    parsed_url = urlparse(url)

    safe_path = urls.url_fix(parsed_url.path)

    return parsed_url.scheme + '://' + parsed_url.netloc + safe_path


def find_base_domain(url):
    """
    Method to extract the base domain of the provided url
    :param url: The url to extract the domain from
    :return: The base domain of the provided url
    """
    parsed_url = urlparse(url)

    return parsed_url.netloc


def main():

    def __init__():
        parser = argparse.ArgumentParser(description='This is a script to crawl a website and '
                                                     'display the static assets on each page.')
        parser.add_argument('-u', '--url', help='A url to crawl.', required=True)
        return parser.parse_args()

    # calls the initialisation function of main to read the command line arguments
    args = __init__()

    safe_url = make_url_safe(args.url)

    base_domain = find_base_domain(safe_url)

    site_map = create_site_map(base_domain)

    print(site_map)

    # for item in site_map:
    #     if item.url:
    #         site_map[item][assets] = extract_static_assets(item.url)
    #     for subdomain in item.subdomain:
    #         site_map[subdomain][assets] = extract_static_assets(subdomain.url)

    # print(site_map)


(__name__ == '__main__' and main())
