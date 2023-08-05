# -*- coding: utf-8 -*-
"""Migration steps for plone.mls.listing."""

from plone import api
from plone.browserlayer import utils as layerutils
from plone.mls.listing import PRODUCT_NAME
from plone.mls.listing.browser.interfaces import IListingSpecific
from plone.mls.listing.browser.listing_collection import CONFIGURATION_KEY
from plone.mls.listing.browser.listing_collection import IListingCollection
from plone.mls.listing.interfaces import IMLSAgencyContactInformation
from plone.mls.listing.interfaces import IMLSUISettings
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import logging
import pkg_resources


logger = logging.getLogger(PRODUCT_NAME)

LISTING_TYPE = 'plone.mls.listing.listing'
PROFILE_ID = 'profile-plone.mls.listing:default'


def convert_value_to_token(
    obj=None, request=None, value=None, vocab=None, loc_type=None,
):
    """Helper method to convert values into tokens."""
    token_values = []
    log_msg = None
    value_dec = value.encode('utf-8').decode('unicode_escape')
    for term in vocab:
        if value == term.title or value_dec == term.title:
            token_values.append(term.token)

    if len(token_values) == 0:
        token_values = [value]
        log_msg = (
            u'No ListingCollection entry found for {0}: \'{1}\'. '
            u'Please check: {2}'.format(
                loc_type,
                value,
                obj.absolute_url(),
            )
        )
    elif len(token_values) > 1:
        log_msg = (
            u'Warning: multiple values match the previously '
            u'selected {0} name of \'{1}\': {2}'.format(
                loc_type,
                value,
                obj.absolute_url(),
            )
        )
    if log_msg:
        # add message to log
        logger.warn(log_msg)
        # add visible status message in Plone
        api.portal.show_message(
            message=log_msg,
            request=request,
            type='warn',
        )

    return tuple(token_values)


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Update TinyMCE linkable types.
    * Update Kupu linkable types if available.
    """
    tinymce = api.portal.get_tool(name='portal_tinymce')
    if tinymce is not None:
        if LISTING_TYPE not in tinymce.linkable:
            tinymce.linkable += '\n' + LISTING_TYPE

    portal_types = api.portal.get_tool(name='portal_types')
    kupu = api.portal.get_tool(name='kupu_library_tool')
    if kupu is not None:
        linkable = list(kupu.getPortalTypesForResourceType('linkable'))
        if LISTING_TYPE not in linkable:
            # Kupu's resource list can accumulate old, no longer valid types.
            # It will throw an exception if we try to resave them.
            # So, let's clean the list.
            valid_types = dict([
                (t.id, 1) for t in portal_types.listTypeInfo()
            ])
            linkable = [pt for pt in linkable if pt in valid_types]

            linkable.append(LISTING_TYPE)
            kupu.updateResourceTypes(({
                'resource_type': 'linkable',
                'old_type': 'linkable',
                'portal_types': linkable,
            },))


def migrate_to_1002(context):
    """Migrate from 1001 to 1002.

    * Add plone.mls.listing.listing to Article's allowd types.
    * Add versioning behavior.
    * Enable versioning in portal types.
    """
    portal_types = api.portal.get_tool(name='portal_types')
    quickinstaller = api.portal.get_tool(name='portal_quickinstaller')

    # 1. Add plone.mls.featured.featured to Article's allowd types.
    if quickinstaller.isProductInstalled('raptus.article.core'):
        article = portal_types.get('Article', None)
        if article is None:
            return
        if LISTING_TYPE not in article.allowed_content_types:
            article.allowed_content_types += (LISTING_TYPE, )

    # 2. Add versioning behavior.
    try:
        import plone.app.versioningbehavior
        plone.app.versioningbehavior  # pyflakes
    except ImportError:
        pass
    else:
        listing = portal_types.get(LISTING_TYPE, None)
        if listing is None:
            return

        versioning_behavior = 'plone.app.versioningbehavior.behaviors.' \
                              'IVersionable'
        if versioning_behavior not in listing.behaviors:
            listing.behaviors += (versioning_behavior, )

    try:
        from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
        # we're on plone < 4.1, configure versionable types manually
    except ImportError:
        # repositorytool.xml will be used
        pass
    else:
        # 3. Enable versioning in portal types.
        portal_repository = api.portal.get_tool(name='portal_repository')
        versionable = list(portal_repository.getVersionableContentTypes())
        if LISTING_TYPE not in versionable:
            # Use append() to make sure we don't overwrite any content types
            # which may already be under version control.
            versionable.append(LISTING_TYPE)
            # Add default versioning policies to the versioned type.
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(LISTING_TYPE,
                                                          policy_id)
        portal_repository.setVersionableContentTypes(versionable)


def migrate_to_1003(context):
    """Migrate from 1002 to 1003.

    * Add plone.mls.listing browser layer.
    * Register custom stylesheet.
    """
    if IListingSpecific not in layerutils.registered_layers():
        layerutils.register_layer(IListingSpecific, name='plone.mls.listing')

    portal_css = api.portal.get_tool(name='portal_css')
    stylesheet_id = '++resource++plone.mls.listing.stylesheets/main.css'
    portal_css.registerStylesheet(stylesheet_id, media='screen')


def migrate_to_1004(context):
    """Migrate from 1003 to 1004.

    * Set 'Link using UIDs' for TinyMCE to false.
    """
    tinymce = api.portal.get_tool(name='portal_tinymce')
    if tinymce is not None:
        tinymce.link_using_uids = False


def migrate_to_1005(context):
    """Migrate from 1004 to 1005.

    * Register 'Agent Information' portlet.
    * Activate portal actions.
    * Register JS resources.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    setup.runImportStepFromProfile(PROFILE_ID, 'actions')
    setup.runImportStepFromProfile(PROFILE_ID, 'portlets')


def migrate_to_1006(context):
    """Migrate from 1005 to 1006.

    * Register 'Agent Contact' portlet.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'portlets')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    setup.runImportStepFromProfile(PROFILE_ID, 'controlpanel')


def migrate_to_1007(context):
    """Migrate from 1006 to 1007.

    * Update the IMLSAgencyContactInformation registry settings.
    """
    registry = getUtility(IRegistry)
    registry.registerInterface(IMLSAgencyContactInformation)


def migrate_to_1008(context):
    """Migrate from 1007 to 1008.

    * Update portal actions.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'actions')
    registry = getUtility(IRegistry)
    registry.registerInterface(IMLSAgencyContactInformation)


def migrate_to_1009(context):
    """Migrate from 1008 to 1009.

    * Add the IMLSUIInformation registry settings.
    * Install ps.plone.fotorama.
    """
    try:
        item = 'ps.plone.fotorama'
        pkg_resources.get_distribution(item)
    except pkg_resources.DistributionNotFound:
        pass
    else:
        quickinstaller = api.portal.get_tool(name='portal_quickinstaller')
        if not quickinstaller.isProductInstalled(item):
            if quickinstaller.isProductInstallable(item):
                quickinstaller.installProduct(item)
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    setup.runImportStepFromProfile(PROFILE_ID, 'controlpanel')


def migrate_to_1010(context):
    """"Migrate from 1009 to 1010

    * update java sscript registry
    * update css registry
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def migrate_to_1011(context):
    """"Migrate from 1010 to 1011

    * update css registry
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def migrate_to_1012(context):
    """"Migrate from 1011 to 1012

    * update javascript & css registry
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def migrate_to_1013(context):
    """"Migrate from 1012 to 1013

    * update existing ListingCollections
    """
    request = getattr(context, 'REQUEST', None)
    languages = api.portal.get_tool(name='portal_languages')

    state_vocab_factory = getUtility(
        IVocabularyFactory,
        'plone.mls.listing.LocationStates',
    )
    county_vocab_factory = getUtility(
        IVocabularyFactory,
        'plone.mls.listing.LocationCounties',
    )
    district_vocab_factory = getUtility(
        IVocabularyFactory,
        'plone.mls.listing.LocationDistricts',
    )
    catalog = api.portal.get_tool(name='portal_catalog')

    for language in languages.getSupportedLanguages():
        logger.info(
            'Searching for Listing Collections in '
            'language \'{0}\''.format(language))
        search_results = catalog(
            Language=language,
            object_provides=IListingCollection.__identifier__,
        )

        for brain in search_results:
            obj = brain.getObject()
            logger.info(
                'Migrating Listing Collection: {0}'.format(obj.absolute_url()))
            annotations = IAnnotations(obj)
            content = annotations.get(CONFIGURATION_KEY, None)
            if content is None:
                continue

            district = content.get('location_district', None)
            county = content.get('location_county', None)
            state = content.get('location_state', None)

            if isinstance(district, basestring):
                vocab = district_vocab_factory(obj)
                token_values = convert_value_to_token(
                    obj=obj,
                    request=request,
                    value=district,
                    vocab=vocab,
                    loc_type='district',
                )
                content['location_district'] = token_values

            if isinstance(county, basestring):
                vocab = county_vocab_factory(obj)
                token_values = convert_value_to_token(
                    obj=obj,
                    request=request,
                    value=county,
                    vocab=vocab,
                    loc_type='county',
                )
                content['location_county'] = token_values

            if isinstance(state, basestring):
                vocab = state_vocab_factory(obj)
                token_values = convert_value_to_token(
                    obj=obj,
                    request=request,
                    value=state,
                    vocab=vocab,
                    loc_type='state',
                )
                content['location_state'] = token_values

            annotations[CONFIGURATION_KEY] = content


def migrate_to_1014(context):
    """"Migrate from 1013 to 1014

    * Update viewlets
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'viewlets')


def migrate_to_1015(context):
    """"Migrate from 1014 to 1015

    * Update JS registry.
    """
    try:
        js = api.portal.get_tool(name='portal_javascripts')
    except AttributeError:
        pass
    else:
        js.unregisterResource(
            'http://maps.google.com/maps/api/js?sensor=false',
        )
        js.unregisterResource(
            'https://maps-api-ssl.google.com/maps/api/js?sensor=false',
        )


def migrate_to_1016(context):
    """"Migrate from 1015 to 1016.

    * Update plone.mls.listing settings.
    """
    setup = api.portal.get_tool(name='portal_setup')

    try:
        from plone.portlets.utils import unregisterPortletType
        unregisterPortletType(context, 'portlets.AgentContact')
        unregisterPortletType(context, 'portlets.AgentInformation')
        unregisterPortletType(context, 'portlets.QuickSearch')
    except ImportError:
        pass
    else:
        setup.runImportStepFromProfile(PROFILE_ID, 'portlets')


def migrate_to_1017(context):
    """"Migrate from 1016 to 1017.

    * Update plone.mls.listing settings.
    """
    registry = getUtility(IRegistry)
    registry.registerInterface(IMLSUISettings)
