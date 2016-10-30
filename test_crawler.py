#!/usr/bin/env python

import unittest
import crawler
from crawler import make_url_safe, find_base_domain


class TestCrawler(unittest.TestCase):

    def test_make_url_safe(self):

        url = 'https://www.test.com'
        self.assertEqual(make_url_safe(url), 'https://www.test.com')

        url = 'www.test.com/foo bar'
        self.assertEqual(make_url_safe(url), 'http://www.test.com/foo%20bar')


    def test_find_base_domain(self):

        url = 'http://www.test.com/foo'
        self.assertEqual(find_base_domain(url), 'www.test.com')


if __name__ == '__main__':
    unittest.main()
