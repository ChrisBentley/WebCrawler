#!/usr/bin/env python

"""
Program that accepts and url and creates a site map of of the domain.
Static Assets of each page are displayed.

Author: Chris Bentley
"""

import argparse
import pprint
from urllib import robotparser
from urllib.request import urlopen, HTTPError
from urllib.parse import urlparse
from werkzeug import urls
from bs4 import BeautifulSoup


def create_site_map(url):
    """
    Method to create a site map for a given url
    :param url: The url of the site to create a map of
    :return: JSON object containing a site map of unique urls
    """
    site_map = {}
    links_visited = []
    base_domain = find_base_domain(url)

    rp = robotparser.RobotFileParser()
    rp.set_url('http://' + base_domain + '/robots.txt')
    rp.read()

    # Get an initial set of links to explore from the base domain of the provided url
    initial_page_links = extract_page_links(get_html_data(url), base_domain, rp)

    all_page_links = unique(initial_page_links)

    while len(links_visited) < len(all_page_links):

        new_page_links = all_page_links

        for link in new_page_links:
            if link not in links_visited:
                links_visited.append(link)
                html_data = get_html_data(link)

                static_assets = extract_static_assets(html_data)
                site_map[link] = static_assets

                newly_discovered_links = extract_page_links(html_data, base_domain, rp)

                all_page_links += newly_discovered_links
                all_page_links = unique(all_page_links)

                print('Unique URLs Found = {}'.format(len(all_page_links)))
                print('Unique URLs Visited = {}'.format(len(links_visited)))

    return site_map


def unique(list_of_links):
    """
    Method to make sure all links in a list are unique
    :param list_of_links: A list of urls
    :return: A unique list of urls
    """
    return list(set(list_of_links))


def get_html_data(url):
    """
    Method to get html data from a provided url
    :param url: A url to download data from
    :return: Raw html data downloaded from the url
    """
    print('Downloading HTML from - {}'.format(url))
    try:
        site = urlopen(url)
        html_data = site.read()
    except HTTPError as e:
        if e.code == 404:
            print('404 Not Found error occurred - continuing...')
            return None
        elif e.code == 403:
            print('403 Forbidden error occurred - continuing...')
            return None
        else:
            raise

    return html_data


def extract_page_links(html_data, base_domain, rp):
    """
    Method to extract all the url links from html data
    :param html_data: Raw HTML from a website
    :param base_domain: The base domain to check links against
    :param rp: Initialised robotparser object
    :return: A list of safe links that were found in the html data
    """
    page_links = []

    if html_data is None:
        return page_links

    # TODO: Check if lxml makes a large performance difference.
    soup = BeautifulSoup(html_data, 'html.parser')

    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is None:
            continue
        if len(link_url) < 1:
            continue
        if 'mailto' in link_url:
            continue
        if rp.can_fetch('*', link_url) is False:
            continue

        if link_url[0] == '/':
            page_links.append(make_url_safe(base_domain + link_url))
        else:
            if base_domain in find_base_domain(link_url):
                page_links.append(link.get('href'))

    return page_links


def extract_static_assets(html_data):
    """
    Method to extract all the static assets for a given url
    :param html_data: Raw HTML from a website
    :return: Array containing a list of static assets found in the html data
    """
    static_assets = []

    if html_data is None:
        return static_assets

    soup = BeautifulSoup(html_data, 'html.parser')

    # Find all static images
    images = soup.find_all('img')
    for image in images:
        static_assets.append(image.get('src'))

    # Fina all static scripts
    scripts = soup.find_all('script')
    for script in scripts:
        if script.get('src') is not None:
            static_assets.append(script.get('src'))

    # find all static links
    links = soup.find_all('link')
    for link in links:
        if 'stylesheet' in link.get('rel'):
            static_assets.append(link.get('href'))
            continue
        if 'icon' in link.get('rel'):
            static_assets.append(link.get('href'))
            continue
        if 'apple-touch-icon-precomposed' in link.get('rel'):
            static_assets.append(link.get('href'))

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

    # Calls the initialisation function of main to read the command line arguments
    args = __init__()

    safe_url = make_url_safe(args.url)

    site_map = create_site_map(safe_url)

    pprint.pprint(site_map)


(__name__ == '__main__' and main())
