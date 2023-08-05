# -*- coding: utf-8 -*-
"""Recent MLS Listings."""

from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.memoize.view import memoize
from plone.mls.core.navigation import ListingBatch
from plone.mls.listing import AnnotationStorage
from plone.mls.listing import PLONE_4
from plone.mls.listing import PLONE_5
from plone.mls.listing.api import prepare_search_params
from plone.mls.listing.api import recent_listings
from plone.mls.listing.browser.interfaces import IBaseListingItems
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.i18n import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form.browser import checkbox
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.interface import noLongerProvides
from zope.traversing.browser.absoluteurl import absoluteURL


CONFIGURATION_KEY = 'plone.mls.listing.recentlistings'


class IPossibleRecentListings(Interface):
    """Marker interface for possible RecentListings viewlet."""


class IRecentListings(IBaseListingItems):
    """Marker interface for RecentListings viewlet."""


class RecentListingsViewlet(ViewletBase):
    """Show recent MLS listings."""

    _listings = None
    _batching = None

    if PLONE_5:
        index = ViewPageTemplateFile('templates/p5_listing_results.pt')
    elif PLONE_4:
        index = ViewPageTemplateFile('templates/recent_listings_viewlet.pt')

    @property
    def available(self):
        return IRecentListings.providedBy(self.context) and \
            not IListingDetails.providedBy(self.view)

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY, {})

    def update(self):
        """Prepare view related data."""
        super(RecentListingsViewlet, self).update()
        self.context_state = queryMultiAdapter((self.context, self.request),
                                               name='plone_context_state')

        self.limit = self.config.get('limit', 25)
        self._get_listings()

    def _get_listings(self):
        """Query the recent listings from the MLS."""
        params = {
            'limit': self.limit,
            'offset': self.request.get('b_start', 0),
            'lang': self.portal_state.language(),
        }
        params.update(self.config)
        params = prepare_search_params(params)
        results, batching = recent_listings(
            params=params,
            context=self.context,
            config=self.config,
        )
        self._listings = results
        self._batching = batching

    @property
    def layout_css(self):
        if self.config.get('grid_layout', False):
            return u'listing-grid-view'
        return u''

    @property
    @memoize
    def listings(self):
        """Return listing results."""
        return self._listings

    @memoize
    def view_url(self):
        """Generate view url."""
        if not self.context_state.is_view_template():
            url = self.context_state.current_base_url()
        else:
            url = absoluteURL(self.context, self.request)
        if not url.endswith('/'):
            url = url + '/'
        return url

    @property
    def batching(self):
        return ListingBatch(self.listings, self.limit,
                            self.request.get('b_start', 0), orphan=1,
                            batch_data=self._batching)


class IRecentListingsConfiguration(Interface):
    """Recent Listings Configuration Form."""

    grid_layout = schema.Bool(
        description=_(
            u'If allowed by the theme/design, the listings will be displayed '
            u'in a grid layout when enabled.',
        ),
        default=False,
        required=False,
        title=_(u'Grid Layout'),
    )

    agency_listings = schema.Bool(
        description=_(
            u'If activated, only listings of the configured agency are shown.',
        ),
        required=False,
        title=_(u'Agency Listings'),
    )

    agency_priority = schema.Bool(
        description=_(
            u'If selected, the results will first display the listings from '
            u'this agency and then display the rest of the applicable '
            u'listings. This option will supersede the \'Agency Listings\' '
            u'option if selected.',
        ),
        required=False,
        title=_(u'Agency Priority Ordering'),
    )

    show_unverified = schema.Bool(
        default=False,
        required=False,
        title=_(u'Show Unverified Listings'),
    )

    show_unverified_only = schema.Bool(
        description=_(
            u'"Show Unverified Listings" must be activated to take effect.',
        ),
        default=False,
        required=False,
        title=_(u'Only Show Unverified Listings'),
    )

    listing_type = schema.List(
        required=False,
        title=_(u'Listing Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.ListingTypes',
        ),
    )

    price_min = schema.Int(
        description=_(
            u'Enter the minimum price for listings. If no price is given, all '
            u'listings from the lowest price are shown.',
        ),
        required=False,
        title=_(u'Price (Min)'),
    )

    price_max = schema.Int(
        description=_(
            u'Enter the maximum price for listings. If no price is given, all '
            u'listings to the highest price are shown.',
        ),
        required=False,
        title=_(u'Price (Max)'),
    )

    limit = schema.Int(
        default=25,
        required=False,
        title=_(u'Items per Page'),
    )

    zoomlevel = schema.Int(
        default=7,
        required=False,
        title=_(u'Zoomlevel for google-maps '),
    )


class RecentListingsConfiguration(form.Form):
    """Recent Listings Configuration Form."""

    fields = field.Fields(IRecentListingsConfiguration)
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    label = _(u"'Recent Listings' Configuration")
    description = _(
        u"Adjust the behaviour for this 'Recent Listings' viewlet.",
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        content = annotations.get(
            CONFIGURATION_KEY,
            annotations.setdefault(CONFIGURATION_KEY, {}),
        )
        content = AnnotationStorage(content)
        content.context = self.context
        return content

    @button.buttonAndHandler(_(u'Save'))
    def handle_save(self, action):
        data, errors = self.extractData()
        if not errors:
            annotations = IAnnotations(self.context)
            annotations[CONFIGURATION_KEY] = data
            self.request.response.redirect(absoluteURL(self.context,
                                                       self.request))

    @button.buttonAndHandler(_(u'Cancel'))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))


class RecentListingsStatus(object):
    """Return activation/deactivation status of RecentListings viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleRecentListings.providedBy(self.context) and \
            not IRecentListings.providedBy(self.context)

    @property
    def active(self):
        return IRecentListings.providedBy(self.context)


class RecentListingsToggle(object):
    """Toggle RecentListings viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IRecentListings.providedBy(self.context):
            # Deactivate RecentListings viewlet.
            noLongerProvides(self.context, IRecentListings)
            self.context.reindexObject(idxs=['object_provides'])
            msg = _(u"'Recent Listings' viewlet deactivated.")
        elif IPossibleRecentListings.providedBy(self.context):
            alsoProvides(self.context, IRecentListings)
            self.context.reindexObject(idxs=['object_provides'])
            msg = _(u"'Recent Listings' viewlet activated.")
        else:
            msg = _(
                u'The \'Recent Listings\' viewlet does\'t work with this '
                u'content type. Add \'IPossibleRecentListings\' to the '
                u'provided interfaces to enable this feature.',
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
