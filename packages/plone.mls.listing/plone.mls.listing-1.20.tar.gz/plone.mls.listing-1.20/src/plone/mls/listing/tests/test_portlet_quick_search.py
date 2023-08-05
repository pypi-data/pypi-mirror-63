# -*- coding: utf-8 -*-
"""Test plone.mls.listing Quick Search portlet."""

from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.mls.listing.portlets import quick_search
from plone.mls.listing.testing import PLONE_MLS_LISTING_INTEGRATION_TESTING
from plone.portlets import interfaces
from zope.component import getMultiAdapter
from zope.component import getUtility


try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestQuickSearchPortlet(unittest.TestCase):
    """Test Case for the Quick Search portlet."""

    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))
        self.portlet = getUtility(
            interfaces.IPortletType, name='portlets.QuickSearch',
        )

    def test_portlet_type_registered(self):
        self.assertEqual(self.portlet.addview, 'portlets.QuickSearch')

    def test_interfaces(self):
        portlet = quick_search.Assignment()
        self.assertTrue(interfaces.IPortletAssignment.providedBy(portlet))
        self.assertTrue(
            interfaces.IPortletDataProvider.providedBy(portlet),
        )

    def test_invoke_add_view(self):
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for item in mapping.keys():
            del mapping[item]
        addview = mapping.restrictedTraverse('+/' + self.portlet.addview)
        addview.createAndAdd(data={})
        self.assertEqual(len(mapping), 1)
        self.assertTrue(
            isinstance(mapping.values()[0], quick_search.Assignment),
        )

    def test_invoke_edit_view(self):
        request = self.layer['request']
        mapping = PortletAssignmentMapping()
        mapping['foo'] = quick_search.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertIsInstance(editview, quick_search.EditForm)

    def test_renderer(self):
        request = self.layer['request']
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(
            interfaces.IPortletManager,
            name='plone.rightcolumn',
            context=self.portal,
        )
        assignment = quick_search.Assignment()
        renderer = getMultiAdapter(
            (self.portal, request, view, manager, assignment),
            interfaces.IPortletRenderer,
        )
        self.assertIsInstance(renderer, quick_search.Renderer)


class TestRenderer(unittest.TestCase):
    """Test Case for the Quick Search portlet renderer."""

    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.layer['request']
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            interfaces.IPortletManager,
            name='plone.rightcolumn',
            context=self.portal,
        )
        assignment = assignment or quick_search.Assignment()

        return getMultiAdapter(
            (context, request, view, manager, assignment),
            interfaces.IPortletRenderer,
        )

    def test_title(self):
        r = self.renderer(
            context=self.portal,
            assignment=quick_search.Assignment(),
        )
        self.assertEqual('Listing Search', r.title)

    def test_custom_title(self):
        r = self.renderer(
            context=self.portal,
            assignment=quick_search.Assignment(heading=u'My Title'),
        )
        self.assertEqual('My Title', r.title)
