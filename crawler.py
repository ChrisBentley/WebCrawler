#!/usr/bin/env python

"""
Program that accepts and url and creates a site map of of the domain.
Static Assets of each page are displayed.

Author: Chris Bentley
"""

import argparse
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

    initial_page_links = extract_page_links(get_html_data(url), base_domain)

    all_page_links = unique(initial_page_links)

    while len(links_visited) < len(all_page_links):

        new_page_links = all_page_links

        for link in new_page_links:
            if link not in links_visited:
                all_page_links += extract_page_links(get_html_data(link), base_domain)
                links_visited.append(link)
                all_page_links = unique(all_page_links)

                print('Unique Pages Found = {}'.format(len(all_page_links)))
                print('Unique Pages Visited = {}'.format(len(links_visited)))

    print(all_page_links)

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
    Method to extract all the url links from html data
    :param html_data: raw HTML from a website
    :return: A list of safe links that were found in the html data
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


def extract_page_links(html_data, base_domain):
    """
    Method to extract all the url links from html data
    :param html_data: Raw HTML from a website
    :param base_domain: The base domain to check links against
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

        if link_url[0] == '/':
            page_links.append(make_url_safe('www.gocardless.com' + link_url))
        else:
            if base_domain in find_base_domain(link_url):
                page_links.append(link.get('href'))

    return page_links


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

    # Calls the initialisation function of main to read the command line arguments
    args = __init__()

    safe_url = make_url_safe(args.url)

    site_map = create_site_map(safe_url)

    # print(site_map)

    # for item in site_map:
    #     if item.url:
    #         site_map[item][assets] = extract_static_assets(item.url)
    #     for subdomain in item.subdomain:
    #         site_map[subdomain][assets] = extract_static_assets(subdomain.url)

    # print(site_map)


(__name__ == '__main__' and main())
