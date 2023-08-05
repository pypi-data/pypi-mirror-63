# -*- coding: utf-8 -*-
"""Vocabulary definitions."""

from plone import api as plone_api
from plone.mls.core import api
from plone.mls.listing import AnnotationStorage
from plone.mls.listing.api import search_options
from plone.mls.listing.browser import listing_search
from plone.mls.listing.i18n import _
from plone.mls.listing.interfaces import IMLSVocabularySettings
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


ROOM_VALUES = [
    ('--MINVALUE--', _(u'Min')),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    ('--MAXVALUE--', _(u'Max')),
]

LOT_SIZE_VALUES = [
    ('--MINVALUE--', _(u'Min')),
    (500, u'500 m²'),
    (1000, u'1000 m²'),
    (2000, u'2000 m²'),
    (4000, u'4000 m²'),
    (6000, u'6000 m²'),
    (8000, u'8000 m²'),
    (10000, u'1 hec'),
    (20000, u'2 hec'),
    (100000, u'10 hec'),
    ('--MAXVALUE--', _(u'Max')),
]

INTERIOR_AREA_VALUES = [
    ('--MINVALUE--', _(u'Min')),
    (50, u'50 m²'),
    (100, u'100 m²'),
    (150, u'150 m²'),
    (250, u'250 m²'),
    (500, u'500 m²'),
    (750, u'750 m²'),
    (1000, u'1000 m²'),
    (1250, u'1250 m²'),
    (1500, u'1500 m²'),
    ('--MAXVALUE--', _(u'Max')),
]

SORT_INDICES = [
    ('size_under_roof_area', u'Area Under Roof'),
    ('number_of_bedrooms', u'Bedrooms'),
    ('sortable_city', u'City'),
    ('location_country', u'Country'),
    ('location_county', u'County'),
    ('location_district', u'District'),
    ('development', u'Development'),
    ('size_interior_area', u'Interior Area (CS, CL)'),
    ('last_activated_date', u'Last Activated Date'),
    ('size_living_area', u'Living Area (RS, RL)'),
    ('size_lot', u'Lot Size'),
    ('price_asking', u'Price Asking (RS, CS, LL)'),
    ('price_high_season_month', u'Price High Season Month (RL)'),
    ('price_low_season_month', u'Price Low Season Month (RL)'),
    ('price_longterm_month', u'Price Longterm Month (CL)'),
    ('number_of_rooms', u'Rooms'),
    ('sleeping_capacity', u'Sleeping Capacity'),
    ('location_state', u'State'),
    ('sortable_title', u'Title'),
    ('unit_floor', u'Unit Floor'),
    ('sortable_workflow_state', u'Workflow Status'),
    ('year_built', u'Year Built'),
]

WORKFLOW_STATE_VALUES = [
    ('Active', u'Active'),
    ('PendingSale', u'PendingSale'),
    ('Sold', u'Sold'),
]


@implementer(IVocabularyFactory)
class AvailableListingSearches(object):
    """Vocabulary which returns all available listing searches."""

    def __call__(self, context):
        brains = plone_api.content.find(
            object_provides=listing_search.IListingSearch,
            sort_on='sortable_title',
        )
        items = []
        for brain in brains:
            title = '{0} ({1})'.format(brain.Title, brain.getPath())
            items.append(SimpleTerm(brain.UID, brain.UID, title))
        return SimpleVocabulary(items)


AvailableListingSearchesFactory = AvailableListingSearches()


@implementer(IVocabularyFactory)
class BasePriorityVocabulary(object):
    """Vocabulary factory with optional priority list.

    data = [
        ('x1', 'a1'),
        ('x3', 'a3'),
        ('x4', 'a4'),
        ('x2', 'a2'),
        ('x5', 'a5'),
    ]

    priority = ['x5', 'x3']

    data_sorted = [
        ('x5', 'a5'),
        ('x3', 'a3'),
        ('x1', 'a1'),
        ('x2', 'a2'),
        ('x4', 'a4'),
    ]

    def sort_data(data_arg, priority_arg):
        def get_key(item):
            if item[0] in priority_arg:
                return '__{0:03d}'.format(priority_arg.index(item[0]))
            return item[1]

        data_arg.sort(key=get_key)

        assert data_arg == data_sorted

    sort_data(data, priority)
    """

    priority = ''
    vocabulary_name = None
    local_settings_key = None
    filter_key = ''

    def _sort(self, data, priority):
        """Sort list of tuple by keys in priority list or value otherwise."""

        def get_key(item):
            if item[0] in priority:
                return '__{0:03d}'.format(priority.index(item[0]))
            return u'__1{0}'.format(item[1])

        if len(priority) > 0:
            data.sort(key=get_key)
        else:
            data.sort(key=lambda item: item[1])

        return data

    def __call__(self, context):
        if isinstance(context, AnnotationStorage):
            context = context.context

        portal_state = queryMultiAdapter(
            (context, getRequest()),
            name='plone_portal_state',
        )
        registry = getUtility(IRegistry)
        try:
            settings = registry.forInterface(  # noqa
                IMLSVocabularySettings,
                check=False,
            )
        except KeyError:
            priority_list = []
        else:
            value = getattr(settings, self.priority, '')
            if value is None:
                value = ''
            priority_list = [
                item.strip() for item in value.split(',')
                if len(item.strip()) > 0
            ]

        mls_settings = api.get_settings(context=context)
        mls_url = mls_settings.get('mls_site', None)

        try:
            language = portal_state.language()
        except Exception:
            language = None

        types = search_options(
            mls_url, self.vocabulary_name,
            language,
            context=context,
        )

        if self.local_settings_key is not None:
            annotations = IAnnotations(context)

            local_settings = annotations.get(self.local_settings_key, {})
            filtered = local_settings.get(self.filter_key, ())
            if len(filtered) > 0:
                types = [(k, v) for k, v in types if k in filtered]

        terms = []
        if types is not None:
            types = self._sort(types, priority_list)
            terms = [
                SimpleTerm(item[0], item[0], item[1]) for item in types
            ]
        return SimpleVocabulary(terms)


class GeographicTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'geographic_types'."""

    vocabulary_name = 'geographic_types'
    priority = 'geographic_types_priority'


GeographicTypesVocabularyFactory = GeographicTypesVocabulary()


class ListingTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'listing_types'."""

    vocabulary_name = 'listing_types'
    priority = 'listing_types_priority'


ListingTypesVocabularyFactory = ListingTypesVocabulary()


class ListingTypesSearchVocabulary(ListingTypesVocabulary):
    """Priority sortable vocabulary factory for 'listing_types'."""

    local_settings_key = listing_search.CONFIGURATION_KEY
    filter_key = 'listing_type'


ListingTypesSearchVocabularyFactory = ListingTypesSearchVocabulary()


class LocationCountyVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_county'."""

    vocabulary_name = 'location_county'


LocationCountyVocabularyFactory = LocationCountyVocabulary()


class LocationDistrictVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_district'."""

    vocabulary_name = 'location_district'


LocationDistrictVocabularyFactory = LocationDistrictVocabulary()


class LocationStateVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_state'."""

    vocabulary_name = 'location_state'


LocationStateVocabularyFactory = LocationStateVocabulary()


class LocationTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_types'."""

    vocabulary_name = 'location_types'
    priority = 'location_types_priority'


LocationTypesVocabularyFactory = LocationTypesVocabulary()


class ObjectTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'object_types'."""

    vocabulary_name = 'object_types'
    priority = 'object_types_priority'


ObjectTypesVocabularyFactory = ObjectTypesVocabulary()


class OwnershipTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'ownership_types'."""

    vocabulary_name = 'ownership_types'
    priority = 'ownership_types_priority'


OwnershipTypesVocabularyFactory = OwnershipTypesVocabulary()


@implementer(IVocabularyFactory)
class RoomsVocabulary(object):

    def __call__(self, context):
        items = []
        for item in ROOM_VALUES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


RoomsVocabularyFactory = RoomsVocabulary()


class ViewTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'view_types'."""

    vocabulary_name = 'view_types'
    priority = 'view_types_priority'


ViewTypesVocabularyFactory = ViewTypesVocabulary()


@implementer(IVocabularyFactory)
class YesNoAllVocabulary(object):

    def __call__(self, context):
        items = []
        items.append(SimpleTerm('1', '1', _(u'Yes')))
        items.append(SimpleTerm('0', '0', _(u'No')))
        items.append(SimpleTerm('--NOVALUE--', '--NOVALUE--', _(u'All')))
        return SimpleVocabulary(items)


YesNoAllVocabularyFactory = YesNoAllVocabulary()


@implementer(IVocabularyFactory)
class LotSizeVocabulary(object):

    def __call__(self, context):
        items = []
        for item in LOT_SIZE_VALUES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


LotSizeVocabularyFactory = LotSizeVocabulary()


@implementer(IVocabularyFactory)
class InteriorAreaVocabulary(object):

    def __call__(self, context):
        items = []
        for item in INTERIOR_AREA_VALUES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


InteriorAreaVocabularyFactory = InteriorAreaVocabulary()


@implementer(IVocabularyFactory)
class SortIndicesVocabulary(object):

    def __call__(self, context):
        items = []
        for item in SORT_INDICES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


SortIndicesVocabularyFactory = SortIndicesVocabulary()


@implementer(IVocabularyFactory)
class WorkflowStatesVocabulary(object):

    def __call__(self, context):
        items = []
        for item in WORKFLOW_STATE_VALUES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


WorkflowStatesVocabularyFactory = WorkflowStatesVocabulary()
