# -*- coding: utf-8 -*-
"""Test Setup of ps.plone.mls."""

from plone import api
from plone.browserlayer.utils import registered_layers
from ps.plone.mls import PLONE_4
from ps.plone.mls.config import PROJECT_NAME
from ps.plone.mls.testing import INTEGRATION_TESTING


try:
    import unittest2 as unittest
except ImportError:
    import unittest


CSS = [
    '++resource++ps.plone.mls/mls.css',
]

JS = [
    '++resource++ps.plone.mls/mls.js',
]


class TestSetup(unittest.TestCase):
    """Validate setup process for ps.plone.mls."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']

    def test_product_is_installed(self):
        """Validate that our product is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled(PROJECT_NAME))

    def test_addon_layer(self):
        """Validate that the browserlayer for our product is installed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IPloneMLSLayer', layers)

    def test_cssregistry(self):
        """Validate the CSS file registration."""
        if not PLONE_4:
            return

        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertIn(id, resource_ids, '{0} not installed'.format(id))

    def test_jsregistry(self):
        """Validate the JS file registration."""
        if not PLONE_4:
            return

        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JS:
            self.assertIn(id, resource_ids, '{0} not installed'.format(id))

    def test_plone_app_dexterity_installed(self):
        """Validate that plone.app.dexterity is installed."""
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        if qi.isProductAvailable('plone.app.dexterity'):
            self.assertTrue(qi.isProductInstalled('plone.app.dexterity'))
        else:
            self.assertTrue(
                'plone.app.dexterity' in qi.listInstallableProfiles(),
            )

    def test_plone_mls_listing_installed(self):
        """Validate that plone.mls.listing is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.mls.listing'))


class UninstallTestCase(unittest.TestCase):
    """Validate uninstall process for ps.plone.mls."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']

        qi = self.portal.portal_quickinstaller
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECT_NAME])

    def test_product_is_uninstalled(self):
        """Validate that our product is uninstalled."""
        qi = self.portal.portal_quickinstaller
        self.assertFalse(qi.isProductInstalled(PROJECT_NAME))

    def test_addon_layer_removed(self):
        """Validate that the browserlayer is removed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IPloneMLSLayer', layers)

    def test_cssregistry(self):
        """Validate the CSS file unregistration."""
        if not PLONE_4:
            return

        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertNotIn(
                id, resource_ids,
                '{0} is still installed'.format(id),
            )

    def test_jsregistry(self):
        """Validate the JS file unregistration."""
        if not PLONE_4:
            return

        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JS:
            self.assertNotIn(
                id, resource_ids,
                '{0} is still installed'.format(id),
            )
