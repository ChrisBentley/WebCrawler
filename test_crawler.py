#!/usr/bin/env python

import unittest
from urllib import robotparser
from io import StringIO
from unittest.mock import MagicMock, patch

from crawler import(make_url_safe,
                    find_base_domain,
                    unique,
                    get_html_data,
                    extract_page_links,
                    extract_static_assets,
                    create_site_map)

from test_helpers import (TEST_HTML_1,
                        TEST_HTML_2,
                        TEST_HTML_3,
                        EXPECTED_RESULT_FINAL)


class TestCrawler(unittest.TestCase):

    def test_make_url_safe(self):
        url = 'https://www.test.com'
        self.assertEqual(make_url_safe(url), 'https://www.test.com')

        url = 'www.test.com/foo bar'
        self.assertEqual(make_url_safe(url), 'http://www.test.com/foo%20bar')

    def test_find_base_domain(self):
        url = 'http://www.test.com/foo'
        self.assertEqual(find_base_domain(url), 'www.test.com')

    def test_unique(self):
        original_list = ['testing', 'testing']
        expected_list = ['testing']

        self.assertEqual(unique(original_list), expected_list)

    @patch('crawler.urlopen')
    def test_get_html_data(self, urlopen):
        url = 'http://www.test.com'
        output = StringIO(initial_value='testing')
        urlopen.return_value = output

        html_data = get_html_data(url)

        urlopen.assert_called_once_with('http://www.test.com')
        self.assertEqual(html_data, 'testing')

    def test_extract_static_assets(self):
        self.assertEqual(extract_static_assets(None), [])

        expected_assets = ['/css/main.css', '/assets/images/favicon.png', '/assets/images/favicon.png']

        self.assertEqual(extract_static_assets(TEST_HTML_1), expected_assets)

    def test_extract_page_links(self):
        # Overriding the robots.txt parser for this test
        class TestRobotParser(robotparser.RobotFileParser):
            def can_fetch(useragent, url, third):
                return True

        rp = TestRobotParser()

        expected_links = ['http://www.cjbcrazy.com/', 'http://www.cjbcrazy.com/about/']

        self.assertEqual(extract_page_links(TEST_HTML_1, 'www.cjbcrazy.com', rp), expected_links)

    @patch('crawler.get_html_data')
    def test_create_site_map(self, get_html_data):
        url = 'http://www.cjbcrazy.com/'

        expected_result = EXPECTED_RESULT_FINAL

        get_html_data.side_effect = [TEST_HTML_1, TEST_HTML_1, TEST_HTML_2, TEST_HTML_3]

        self.assertEqual(create_site_map(url), expected_result)

if __name__ == '__main__':
    unittest.main()
