#!/usr/bin/env python

"""
Program that accepts and url and creates a site map of of the domain.
Static Assets of each page are displayed.

Author: Chris Bentley
"""

import argparse
from urllib.request import urlopen


def create_site_map(url):
    """
    Method to create a site map for a given url
    :param url: The url containing the domain to create a site map of
    :return: JSON object containing a site map of unique urls
    """

    def __make_url_safe(url):
        return url

    def __find_base_domain(url):
        return url

    site_map = {}

    print(url)

    safe_url = __make_url_safe(url)

    print(safe_url)

    base_domain = __find_base_domain(safe_url)

    print(base_domain)

    return site_map


def extract_static_assets(url):
    """
    Method to extract all the static assets for a given url
    :param url: The url containing the domain to create a site map of
    :return: Array containing a list of static assets
    """
    static_assets = []

    return static_assets


def main():

    def __init__():
        parser = argparse.ArgumentParser(description='This is a script to crawl a website and '
                                                     'display the static assets on each page.')
        parser.add_argument('-u', '--url', help='A url to crawl.', required=True)
        return parser.parse_args()

    # calls the initialisation function of main to read the command line arguments
    args = __init__()

    site_map = create_site_map(args.url)

    print(site_map)

    # for item in site_map:
    #     if item.url:
    #         site_map[item][assets] = extract_static_assets(item.url)
    #     for subdomain in item.subdomain:
    #         site_map[subdomain][assets] = extract_static_assets(subdomain.url)

    # print(site_map)


(__name__ == '__main__' and main())
