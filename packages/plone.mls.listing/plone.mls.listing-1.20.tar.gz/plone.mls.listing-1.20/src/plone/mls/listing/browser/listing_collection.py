# -*- coding: utf-8 -*-
"""MLS Listing collection."""

from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.memoize.view import memoize
from plone.mls.core.navigation import ListingBatch
from plone.mls.listing import AnnotationStorage
from plone.mls.listing import PLONE_4
from plone.mls.listing import PLONE_5
from plone.mls.listing.api import prepare_search_params
from plone.mls.listing.api import search
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


CONFIGURATION_KEY = 'plone.mls.listing.listingcollection'


class IPossibleListingCollection(Interface):
    """Marker interface for possible ListingCollection viewlet."""


class IListingCollection(IBaseListingItems):
    """Marker interface for ListingCollection viewlet."""


class ListingCollectionViewlet(ViewletBase):
    """Dynamic collection of MLS listings."""

    _listings = None
    _batching = None

    if PLONE_5:
        index = ViewPageTemplateFile('templates/p5_listing_results.pt')
    elif PLONE_4:
        index = ViewPageTemplateFile('templates/recent_listings_viewlet.pt')

    @property
    def available(self):
        return IListingCollection.providedBy(self.context) and \
            not IListingDetails.providedBy(self.view)

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY, {})

    def update(self):
        """Prepare view related data."""
        super(ListingCollectionViewlet, self).update()
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
        results, batching = search(
            params=params,
            context=self.context,
            config=self.config,
        )
        self._listings = results
        self._batching = batching

    def total_listings(self):
        if self._batching:
            return self._batching.get('results')
        elif self._listings:
            return len(self._listings)

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


class IListingCollectionConfiguration(Interface):
    """Listing Collection Configuration Form."""

    sort_on = schema.Choice(
        default='last_activated_date',
        required=True,
        title=_(u'Sort by'),
        source='plone.mls.listing.SortIndices',
    )

    reverse = schema.Bool(
        default=True,
        required=False,
        title=_(u'Reverse'),
    )

    grid_layout = schema.Bool(
        description=_(
            u'If allowed by the theme/design, the listings will be displayed '
            u'in a grid layout when enabled.',
        ),
        default=False,
        required=False,
        title=_(u'Grid Layout'),
    )

    overriding_agency_id = schema.TextLine(
        description=_(
            u'Specify an agency ID (or a comma-separated list of multiple '
            u'agency IDs) that will override the Base/Local MLS Settings. If '
            u'left blank, the agency ID from the Base/Local MLS settings will '
            u'be used.',
        ),
        required=False,
        title=_(u'Overriding Agency IDs'),
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

    freetext = schema.TextLine(
        required=False,
        title=_(u'Freetext Search'),
        description=_(
            u'Filter the results by a free text search for location, keywords,'
            u' Listing IDs, and more that can combine results using \'AND\', '
            u'\'OR\', \'NOT\', etc.'),
    )

    listing_type = schema.Tuple(
        default=('cl', 'cs', 'll', 'rl', 'rs'),
        required=False,
        title=_(u'Listing Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.ListingTypes',
        ),
    )

    workflow_state = schema.Tuple(
        default=('Active', 'PendingSale', 'Sold'),
        required=False,
        title=_(u'Workflow Status'),
        value_type=schema.Choice(
            source='plone.mls.listing.WorkflowStates',
        ),
    )

    location_state = schema.Tuple(
        required=False,
        title=_(u'State'),
        value_type=schema.Choice(
            source='plone.mls.listing.LocationStates',
        ),
    )

    location_county = schema.Tuple(
        required=False,
        title=_(u'County'),
        value_type=schema.Choice(
            source='plone.mls.listing.LocationCounties',
        ),
    )

    location_district = schema.Tuple(
        required=False,
        title=_(u'District'),
        value_type=schema.Choice(
            source='plone.mls.listing.LocationDistricts',
        ),
    )

    location_city = schema.TextLine(
        required=False,
        title=_(u'City/Town'),
    )

    price_min = schema.Int(
        required=False,
        title=_(u'Price (Min)'),
    )

    price_max = schema.Int(
        required=False,
        title=_(u'Price (Max)'),
    )

    lot_size_min = schema.Int(
        required=False,
        title=_(u'Lot Size in m² (Min)'),
    )

    lot_size_max = schema.Int(
        required=False,
        title=_(u'Lot Size in m² (Max)'),
    )

    floor_area_min = schema.Int(
        required=False,
        title=_(u'Interior Area in m² (Min)'),
        description=_(
            u'Reminder: All land listings will be excluded once any value is '
            u'set.',
        ),
    )

    floor_area_max = schema.Int(
        required=False,
        title=_(u'Interior Area in m² (Max)'),
    )

    beds_min = schema.Int(
        required=False,
        title=_(u'Bedrooms (Min)'),
        description=_(
            u'Reminder: All land listings will be excluded once any value is '
            u'set as well as any commercial listings with no bedrooms.',
        ),
    )

    beds_max = schema.Int(
        required=False,
        title=_(u'Bedrooms (Max)'),
    )

    baths_min = schema.Int(
        required=False,
        title=_(u'Bathrooms (Min)'),
        description=_(
            u'Reminder: All land listings will be excluded once any value is '
            u'set as well as any commercial listings with no bathrooms.',
        ),
    )

    baths_max = schema.Int(
        required=False,
        title=_(u'Bathrooms (Max)'),
    )

    location_type = schema.Tuple(
        required=False,
        title=_(u'Location Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.LocationTypes',
        ),
    )

    geographic_type = schema.Tuple(
        required=False,
        title=_(u'Geographic Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.GeographicTypes',
        ),
    )

    view_type = schema.Tuple(
        required=False,
        title=_(u'View Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.ViewTypes',
        ),
    )

    object_type = schema.Tuple(
        required=False,
        title=_(u'Object Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.ObjectTypes',
        ),
    )

    ownership_type = schema.Tuple(
        required=False,
        title=_(u'Ownership Type'),
        value_type=schema.Choice(
            source='plone.mls.listing.OwnershipTypes',
        ),
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


class ListingCollectionConfiguration(form.Form):
    """Listing Collection Configuration Form."""

    fields = field.Fields(IListingCollectionConfiguration)
    fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['workflow_state'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget

    label = _(u"'Listing Collection' Configuration")
    description = _(
        u"Adjust the behaviour for this 'Listing Collection' viewlet.",
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
        if errors:
            self.status = self.formErrorsMessage
            return
        annotations = IAnnotations(self.context)
        annotations[CONFIGURATION_KEY] = data
        self.request.response.redirect(absoluteURL(self.context, self.request))

    @button.buttonAndHandler(_(u'Cancel'))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))


class ListingCollectionStatus(object):
    """Return activation/deactivation status of ListingCollection viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleListingCollection.providedBy(self.context) and \
            not IListingCollection.providedBy(self.context)

    @property
    def active(self):
        return IListingCollection.providedBy(self.context)


class ListingCollectionToggle(object):
    """Toggle ListingCollection viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IListingCollection.providedBy(self.context):
            # Deactivate ListingCollection viewlet.
            noLongerProvides(self.context, IListingCollection)
            self.context.reindexObject(idxs=['object_provides'])
            msg = _(u"'Listing Collection' viewlet deactivated.")
        elif IPossibleListingCollection.providedBy(self.context):
            alsoProvides(self.context, IListingCollection)
            self.context.reindexObject(idxs=['object_provides'])
            msg = _(u"'Listing Collection' viewlet activated.")
        else:
            msg = _(
                u'The \'Listing Collection\' viewlet does\'t work with this '
                u'content type. Add \'IPossibleListingCollection\' to the '
                u'provided interfaces to enable this feature.',
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
