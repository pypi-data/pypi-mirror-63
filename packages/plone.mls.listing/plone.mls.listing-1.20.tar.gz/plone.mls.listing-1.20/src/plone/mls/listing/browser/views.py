# -*- coding: utf-8 -*-
"""Various browser views for listings."""

from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.view import memoize
from plone.mls.core import api
from plone.mls.listing import PLONE_4
from plone.mls.listing import PLONE_5
from plone.mls.listing import PRODUCT_NAME
from plone.mls.listing.api import get_agency_info
from plone.mls.listing.api import listing_details
from plone.mls.listing.browser import listing_collection
from plone.mls.listing.browser import listing_search
from plone.mls.listing.browser import recent_listings
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.interfaces import IMLSUISettings
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ps.plone.mls import config
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import NotFound

import copy
import logging
import random


logger = logging.getLogger(PRODUCT_NAME)


MAP_JS = """
var isTouch = false;
var map;

window.addEventListener('touchmove', function MoveDetector() {{
    isTouch = true;
    window.removeEventListener('touchmove', MoveDetector);
    map = initializeMap();
}});

function loadScript(src, callback) {{
  var script = document.createElement("script");
  script.type = "text/javascript";
  if (callback) {{
    script.onload = callback;
  }}
  document.getElementsByTagName("head")[0].appendChild(script);
  script.src = src;
}}


function loadGoogleMaps(callback) {{
  if (typeof google === 'object' && typeof google.maps === 'object') {{
    callback();
  }} else {{
    loadScript('https://maps.googleapis.com/maps/api/js?key={ak}', callback);
  }}
}}


function initializeMap() {{
    var center = new google.maps.LatLng({lat}, {lng});
    var myOptions = {{
        zoom: {zoom},
        center: center,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        mapTypeControl: true,
        disableDoubleClickZoom: true,
        overviewMapControl: true,
        streetViewControl: true,
        scrollwheel: false,
        draggable:!isTouch
    }};

    var map = new google.maps.Map(
        document.getElementById('{map_id}'),
        myOptions
    );

    var has_marker = true;
    if(has_marker) {{
        var myLatlng = new google.maps.LatLng({lat}, {lng});
        var marker = new google.maps.Marker({{
            position: myLatlng,
            map: map
        }});
    }}
    return map;
}};
"""


@implementer(IListingDetails)
class ListingDetails(BrowserView):

    _error = {}
    _data = None
    listing_id = None

    if PLONE_5:
        index = ViewPageTemplateFile('templates/p5_listing_details.pt')
    elif PLONE_4:
        index = ViewPageTemplateFile('templates/listing_details.pt')

    def render(self):
        return self.index()

    def __call__(self):
        self.setup()
        return self.render()

    def setup(self):
        self.portal_state = queryMultiAdapter(
            (self.context, self.request), name='plone_portal_state',
        )
        self.registry = getUtility(IRegistry)
        self._get_data()
        if PLONE_5:
            from Products.CMFPlone.resources import add_resource_on_request
            if self.use_fotorama():
                add_resource_on_request(self.request, 'psplonefotorama')

    @memoize
    def _get_data(self):
        """Get the remote listing data from the MLS."""
        lang = self.portal_state.language()
        if getattr(self.request, 'listing_id', None) is not None:
            self.listing_id = self.request.listing_id
        else:
            self.listing_id = getattr(self.context, 'listing_id', None)
        if self.listing_id:
            self._data = listing_details(
                self.listing_id,
                lang,
                context=self.context,
            )
            if self._data is None:
                raise NotFound(self.context, None, self.request)

    @property
    def data(self):
        return self._data

    @property
    def error(self):
        return self._error

    @property
    def title(self):
        if getattr(self.request, 'listing_id', None) is not None:
            if self.info is not None:
                title = self.info.get('title', None)
                if title is not None:
                    return title.get('value', self.context.title)
        else:
            return self.context.title_or_id()

    @property
    def description(self):
        if self.data is not None:
            return self.data.get('description', None)

    @property
    def agent_quote(self):
        if self.data is not None:
            return self.data.get('agent_quote', None)

    @property
    def long_description(self):
        if self.data is not None:
            return self.data.get('long_description', None)

    @property
    def groups(self):
        if self.data is not None:
            return self.data.get('groups', None)

    @property
    def info(self):
        if self.data is not None:
            return self.data.get('info', None)

    @property
    def lead_image(self):
        if self.data is not None:
            image = self.data.get('images', None)[:1]
            if len(image) > 0:
                return image[0]
        return None

    @property
    def images(self):
        if self.data is not None:
            images = self.data.get('images', None)
            if len(images) > 1:
                return images

    @property
    def video(self):
        if self.data is not None:
            return self.data.get('property_video_embedding', None)

    def is_calendar_visibile(self):
        """Check if the availability calendar can be shown."""
        if self.registry is not None:
            try:
                settings = self.registry.forInterface(IMLSUISettings)  # noqa
            except Exception:
                logger.warning('MLS UI settings not available.')
                return False
        else:
            return False

        # Check if the calender should be shown at all.
        enabled = getattr(settings, 'availability_calendar')
        if not enabled:
            return False

        # Check if the calendar should not be hidden for 3rd party listings.
        agency_only = getattr(settings, 'availability_calendar_agency')
        if not agency_only:
            return True

        # Check if the listing is owned by the agency.
        mls_settings = api.get_settings(context=self.context)
        agency_id = mls_settings.get('agency_id', None)
        contact_data = self.data.get('contact', None)
        agency = contact_data.get('agency', {})
        if agency.get('id', {}).get('value', None) == agency_id:
            return True
        return False

    @property
    def availability_calendar(self):
        if not self.is_calendar_visibile():
            return
        if self.data is not None:
            return self.data.get('availability_calendar', None)

    @property
    def config(self):
        """Get all annotations to for this content."""
        return IAnnotations(self.context)

    def update_agency_info(self, agency, settings):
        # Adjust agency name.
        agency_name = settings.get('agency_name', None)
        if agency_name is not None:
            item = agency.setdefault('name', {})
            item['value'] = agency_name
        else:
            agency['name'] = None

        # Adjust agency logo.
        agency_logo = settings.get('agency_logo_url', None)
        if agency_logo is not None:
            agency['logo'] = agency_logo
        else:
            agency['logo'] = None

        # Adjust agency office phone.
        agency_office_phone = settings.get('agency_office_phone', None)
        if agency_office_phone is not None:
            item = agency.setdefault('office_phone', {})
            item['value'] = agency_office_phone
        else:
            agency['office_phone'] = None

        # Adjust agency website.
        agency_website = settings.get('agency_website', None)
        if agency_website is not None:
            item = agency.setdefault('website', {})
            item['value'] = agency_website
        else:
            agency['website'] = None
        return agency

    def update_agent_info(self, agent, settings):
        # Adjust agent name.
        agent_name = settings.get('agent_name', None)
        if agent_name is not None:
            item = agent.setdefault('name', {})
            item['value'] = agent_name
        else:
            agent['name'] = None

        # Adjust agent title.
        agent_title = settings.get('agent_title', None)
        if agent_title is not None:
            item = agent.setdefault('title', {})
            item['value'] = agent_title
        else:
            agent['title'] = None

        # Adjust agent office phone.
        agent_office_phone = settings.get('agent_office_phone', None)
        if agent_office_phone is not None:
            item = agent.setdefault('agent_office_phone', {})
            item['value'] = agent_office_phone
        else:
            agent['agent_office_phone'] = None

        # Adjust agent cell phone.
        agent_cell_phone = settings.get('agent_cell_phone', None)
        if agent_cell_phone is not None:
            item = agent.setdefault('agent_cell_phone', {})
            item['value'] = agent_cell_phone
        else:
            agent['agent_cell_phone'] = None

        # Adjust agent fax.
        agent_fax = settings.get('agent_fax', None)
        if agent_fax is not None:
            item = agent.setdefault('agent_fax', {})
            item['value'] = agent_fax
        else:
            agent['agent_fax'] = None

        # Adjust agent email.
        agent_email = settings.get('agent_email', None)
        if agent_email is not None:
            item = agent.setdefault('agent_email', {})
            item['value'] = agent_email
        else:
            agent['agent_email'] = None

        # Adjust agent avatar.
        agent_avatar_url = settings.get('agent_avatar_url', None)
        if agent_avatar_url is not None:
            agent['avatar'] = agent_avatar_url
        else:
            agent['avatar'] = None

    @property
    def contact(self):
        if self.data is None:
            return

        mls_settings = api.get_settings(context=self.context)
        agency_id = mls_settings.get('agency_id', None)

        contact_data = self.data.get('contact', None)
        contact_data['overridden'] = False
        agency = contact_data.get('agency', {})
        agent = contact_data.get('agent', {})

        original_agent = self.data.get('original_agent')
        contact_data['original_agent'] = original_agent

        settings = get_agency_info(context=self.context)

        if agency.get('id', {}).get('value', None) == agency_id:
            if settings and settings.get('force', False) is True:
                pass
            else:
                return contact_data

        if settings:
            contact_data['overridden'] = True
            agency = self.update_agency_info(agency, settings)
            agent = self.update_agent_info(agent, settings)

        return contact_data

    def base_url(self):
        items = [
            self.context.absolute_url(),
            getattr(self.request, 'development_id', None),
            getattr(self.request, 'listing_id', None),
        ]
        return '/'.join([item for item in items if item is not None])

    def use_fotorama(self):
        if self.registry is not None:
            try:
                settings = self.registry.forInterface(IMLSUISettings)  # noqa
            except Exception:
                logger.warning('MLS UI settings not available.')
            else:
                return getattr(settings, 'slideshow') == u'fotorama'
        return False

    def use_galleria(self):
        if self.registry is not None:
            try:
                settings = self.registry.forInterface(IMLSUISettings)  # noqa
            except Exception:
                logger.warning('MLS UI settings not available.')
            else:
                return getattr(settings, 'slideshow') == u'galleria'
        # Fallback: 'galleria' is the default.
        return True

    @property
    def map_id(self):
        """Generate a unique css id for the map."""
        info = self.data.get('info', None)
        try:
            item_id = info['id']['value']
        except KeyError:
            item_id = 'unknown'

        return u'map__{0}'.format(item_id)

    @property
    def zoomlevel(self):
        """get the zoomlevel of the context"""
        # default zoomlevel
        zoomlevel = 7
        # check RecentListings settings
        rl = self.config.get(recent_listings.CONFIGURATION_KEY, None)
        if (
            rl is not None and
            recent_listings.IRecentListings.providedBy(self.context)
        ):
            z = rl.get('zoomlevel', None)
            if z is not None:
                zoomlevel = z
        # check ListingCollection settings
        lc = self.config.get(listing_collection.CONFIGURATION_KEY, None)
        if (
            lc is not None and
            listing_collection.IListingCollection.providedBy(self.context)
        ):
            z = lc.get('zoomlevel', None)
            if z is not None:
                zoomlevel = z
        # check ListingSearch settings
        ls = self.config.get(listing_search.CONFIGURATION_KEY, None)
        if (
            ls is not None and
            listing_search.IListingSearch.providedBy(self.context)
        ):
            z = ls.get('zoomlevel', None)
            if z is not None:
                zoomlevel = z

        return zoomlevel

    def javascript_map(self):
        """Return the JS code for the map."""

        info = self.data.get('info', None)
        if info is None:
            return

        geo = info.get('geolocation', None)
        if geo is None:
            return

        try:
            # try to get geo coordinates
            lat, lng = geo.split(',')
        except ValueError:
            # on error no map
            return

        try:
            float(lat)
            float(lng)
        except ValueError:
            return

        return MAP_JS.format(
            lat=unicode(lat),
            lng=unicode(lng),
            map_id=self.map_id,
            zoom=self.zoomlevel,
            ak=self.googleapi,
        )

    @property
    def googleapi(self):
        if self.registry is not None:
            keys = []
            try:
                settings = self.registry.forInterface(IMLSUISettings)  # noqa
            except Exception:
                logger.warning('MLS UI settings not available.')
            else:
                settings_keys = getattr(settings, 'googleapi_additional', []) or []
                keys = copy.copy(settings_keys)
                keys.append(getattr(settings, 'googleapi', ''))
                keys = [
                    key for key in keys if isinstance(key, basestring) and
                    key.strip() != ''
                ]
                return random.choice(keys) or ''
        return ''

    def live_chat_embedding(self):
        """Return embedding code for live chat widget from the development if
        it is enabled.
        """
        dev_cfg = self.config.get(config.SETTINGS_DEVELOPMENT_COLLECTION, {})
        if not dev_cfg.get('enable_live_chat', False):
            return None
        cache = IAnnotations(self.request)
        development = cache.get('ps.plone.mls.development.traversed', None)
        if not development:
            return None
        embedding_code = getattr(development, 'live_chat_embedding', None)
        if embedding_code is not None:
            embedding_code = embedding_code.value
        return embedding_code


class ListingCanonicalURL(ViewletBase):
    """Defines a canonical link relation viewlet to be displayed across the
    site. A canonical page is the preferred version of a set of pages with
    highly similar content. For more information, see:
    https://tools.ietf.org/html/rfc6596
    https://support.google.com/webmasters/answer/139394?hl=en
    """

    @memoize
    def render(self):
        context_state = queryMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        base_url = context_state.current_base_url()
        return u'    <link rel="canonical" href="{0}" />'.format(base_url)
