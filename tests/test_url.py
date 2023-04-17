# -*- encoding: utf-8 -*-
import unittest

import niet.url

VALID_WEBRESOURCES = [
    "https://google.com",
    "http://google.com",
    "https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml",  # noqa
    "http://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml",  # noqa
    "https://herve.beraud.io",
    "http://herve.beraud.io",
    "https://opensource.org/",
    "http://opensource.org/",
]
NONVALID_RESOURCES = [
    "google.com",
    "google.com",
    "raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml",  # noqa
    "raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml",  # noqa
    "herve.beraud.io",
    "herve.beraud.io",
    "opensource.org/",
    "opensource.org/",
]


class TestUrl(unittest.TestCase):
    def test_is_webresource(self):
        for test in VALID_WEBRESOURCES:
            self.assertEqual(True, niet.url.is_webresource(test))

        for test in NONVALID_RESOURCES:
            self.assertEqual(False, niet.url.is_webresource(test))
