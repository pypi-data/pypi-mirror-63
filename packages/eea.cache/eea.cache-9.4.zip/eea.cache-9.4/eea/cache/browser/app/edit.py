""" Browser
"""
from zope import schema
from zope.interface import implementer
from zope.component import adapts, queryMultiAdapter
from z3c.form import form, button, interfaces, util
from plone.supermodel import model
from plone.autoform.form import AutoExtensibleForm
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from eea.cache.interfaces import ICacheAware
from eea.cache.browser.interfaces import VARNISH
from eea.cache.config import EEAMessageFactory as _


class ISettings(model.Schema):
    """ Cache settings
    """
    memcache = schema.Bool(
        title=_(u"Memcache"),
        description=_(u"Invalidate Memcache cache."),
        required=False,
        default=False
    )

    if VARNISH:
        varnish = schema.Bool(
            title=_(u"Varnish"),
            description=_(u"Invalidate Varnish cache."),
            required=False,
            default=False
        )

    relatedItems = schema.Bool(
        title=_(u"Related items"),
        description=_(u"Also invalidate cache for context's related items."),
        required=False,
        default=False
    )

    backRefs = schema.Bool(
        title=_(u"Back references"),
        description=_(u"Also invalidate cache for context's back references."),
        required=False,
        default=False
    )

    redirectURL = schema.URI(
        title=_(u"Redirect URL"),
        description=_(u"Redirect URL when request parameter is present."),
        required=False
    )


@implementer(ISettings)
class SettingsBehavior(object):
    """ Cache invalidation behaviour
    """
    adapts(ICacheAware)

    def __init__(self, context):
        self.context = context
        self._request = None
        self._invalidate_varnish = None
        self._invalidate_memcache = None

    @property
    def invalidate_varnish(self):
        """ Varnish invalidation controller
        """
        if not self._invalidate_varnish:
            self._invalidate_varnish = queryMultiAdapter(
            (self.context, self.request),
            name='varnish.invalidate')
        return self._invalidate_varnish

    @property
    def invalidate_memcache(self):
        """ Memcache invalidation controller
        """
        if not self._invalidate_memcache:
            self._invalidate_memcache = queryMultiAdapter(
                (self.context, self.request),
                name='memcache.invalidate')
        return self._invalidate_memcache

    @property
    def request(self):
        """ REQUEST
        """
        if not self._request:
            self._request = getattr(self.context, 'REQUEST', None)
        return self._request

    @property
    def memcache(self):
        """ Memcache
        """
        return False

    @memcache.setter
    def memcache(self, value):
        """ Invalidate memcache?
        """
        if not value:
            return

        if not self._request:
            self._request = value.get('request', None)

        invalidate_memcache = self.invalidate_memcache
        if invalidate_memcache:
            invalidate_memcache()

    @property
    def varnish(self):
        """ Varnish
        """
        return False

    @varnish.setter
    def varnish(self, value):
        """ Invalidate varnish?
        """
        if not value:
            return

        if not self._request:
            self._request = value.get('request', None)

        invalidate_varnish = self.invalidate_varnish
        if invalidate_varnish:
            invalidate_varnish()

    @property
    def relatedItems(self):
        """ Related items
        """
        return False

    @relatedItems.setter
    def relatedItems(self, value):
        """ Invalidate related items?
        """
        if not value:
            return

        if not self._request:
            self._request = value.get('request', None)

        if value.get('varnish') and self.invalidate_varnish:
            self.invalidate_varnish.relatedItems()
        if value.get('memcache') and self.invalidate_memcache:
            self.invalidate_memcache.relatedItems()

    @property
    def backRefs(self):
        """ Back references
        """
        return False

    @backRefs.setter
    def backRefs(self, value):
        """ Invalidate back references?
        """
        if not value:
            return

        if not self._request:
            self._request = value.get('request', None)

        if value.get('varnish') and self.invalidate_varnish:
            self.invalidate_varnish.backRefs()
        if value.get('memcache') and self.invalidate_memcache:
            self.invalidate_memcache.backRefs()

    @property
    def redirectURL(self):
        """ Redirect URL
        """
        return ''

    @redirectURL.setter
    def redirectURL(self, value):
        """ Redirect URL
        """
        return


class SettingsForm(AutoExtensibleForm, form.EditForm):
    """ Cache settings
    """
    schema = ISettings

    def updateWidgets(self):
        """ Update widgets
        """
        super(SettingsForm, self).updateWidgets()
        self.widgets['redirectURL'].mode = interfaces.HIDDEN_MODE

    def update(self):
        """ Update form
        """
        super(SettingsForm, self).update()
        redirect_url = self.request.get('redirect', '')

        if redirect_url:
            for name, widget in self.widgets.items():
                if name != 'redirectURL':
                    # Select everything by default
                    widget.items[0]['checked'] = True
                else:
                    # Add the redirect URL
                    widget.value = redirect_url

    def applyChanges(self, content, data):
        """ Apply changes
        """
        data['request'] = self.request
        changes = {}
        for name, field in self.fields.items():
            # If the field is not in the data, then go on to the next one
            try:
                newValue = data[name]
            except KeyError:
                continue

            # If the value is NOT_CHANGED, ignore it, since the widget/converter
            # sent a strong message not to do so.
            if newValue is interfaces.NOT_CHANGED:
                continue

            if util.changedField(field.field, newValue, context=content):
                # Only update the data, if it is different
                dm = queryMultiAdapter(
                    (content, field.field), interfaces.IDataManager)

                # Custom behaviour. Send data instead of newValue for more
                # flexibility
                dm.set(data)

                # Record the change using information required later
                changes.setdefault(dm.field.interface, []).append(name)
        return changes

    @button.buttonAndHandler(_('Invalidate'), name='invalidate')
    def invalidate(self, action):
        """ Invalidate cache
        """
        self.status = u""
        msg_invalidated = _(u"Cache invalidated")
        portal_url = getToolByName(self.context, 'portal_url')()
        redirectURL = self.widgets['redirectURL'].value
        data, errors = self.extractData()

        if not redirectURL.startswith(portal_url):
            redirectURL = ''

        if errors:
            self.status = self.formErrorsMessage
            return

        content = self.getContent()
        changes = self.applyChanges(content, data)
        if redirectURL and changes:
            IStatusMessage(self.request).addStatusMessage(msg_invalidated,
                                                          type='info')
            self.request.response.redirect(redirectURL)
        elif changes:
            self.status = msg_invalidated
        else:
            self.status = _(u"Nothing selected to invalidate")
