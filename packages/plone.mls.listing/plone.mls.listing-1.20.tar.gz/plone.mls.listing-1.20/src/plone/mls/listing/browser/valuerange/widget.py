# -*- coding: utf-8 -*-
"""ValueRange Widget Implementation"""

from plone.mls.listing.browser.valuerange.interfaces import IValueRangeWidget
from plone.mls.listing.i18n import _
from z3c.form.browser.widget import addFieldClass
from z3c.form.browser.widget import HTMLTextInputWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import NO_VALUE
from z3c.form.widget import FieldWidget
from z3c.form.widget import SequenceWidget
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.schema.interfaces import IField
from zope.schema.interfaces import ITitledTokenizedTerm


class ValueRangeWidget(HTMLTextInputWidget, SequenceWidget):
    """Value range widget."""
    implementsOnly(IValueRangeWidget)

    klass = u'value-range-widget pat-select2'
    prompt = False

    noValueMessage = _('All')
    promptMessage = _('Select a value...')

    # Internal attributes
    _adapterValueAttributes = SequenceWidget._adapterValueAttributes + \
        ('noValueMessage', 'promptMessage', 'prompt')

    def update(self):
        super(ValueRangeWidget, self).update()
        addFieldClass(self)

    @property
    def maximums(self):
        if self.terms is None:  # update() has not been called yet
            return []
        items = []
        selected = self.maximum

        for count, term in enumerate(self.terms):
            if term.token == '--MINVALUE--':
                continue
            id = '{0}-{1:d}'.format(self.id, count)
            content = term.title or term.value
            if ITitledTokenizedTerm.providedBy(term):
                content = translate(
                    term.title, context=self.request, default=term.title)
            items.append({
                'id': id,
                'value': term.token,
                'content': content,
                'selected': term.token == selected})

#         items.append({
#             'id': self.id + '-novalue',
#             'value': '--MAXVALUE--',
#             'content': u"Max",
#             'selected': selected is None or selected == '--MAXVALUE--',
#         })

        return items

    @property
    def minimums(self):
        if self.terms is None:  # update() has not been called yet
            return ()
        items = []
        selected = self.minimum

#         items.append({
#             'id': self.id + '-novalue',
#             'value': '--MINVALUE--',
#             'content': u"Min",
#             'selected': selected is None or selected == 0,
#         })

        for count, term in enumerate(self.terms):
            if term.token == '--MAXVALUE--':
                continue
            id = '{0}-{1:d}'.format(self.id, count)
            content = term.title or term.value
            if ITitledTokenizedTerm.providedBy(term):
                content = translate(
                    term.title, context=self.request, default=term.title)
            items.append({
                'id': id,
                'value': term.token,
                'content': content,
                'selected': term.token == selected})
        return items

    @property
    def maximum(self):
        maximum = self.request.get(self.name + '-max', None)
        if maximum:
            return maximum
        else:
            return u'--MAXVALUE--'

    @property
    def minimum(self):
        minimum = self.request.get(self.name + '-min', None)
        if minimum:
            return minimum
        else:
            return u'--MINVALUE--'

    def extract(self, default=NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        min_ = self.request.get(self.name + '-min', default)
        max_ = self.request.get(self.name + '-max', default)

        if isinstance(min_, list):
            min_ = min_[0]
        if isinstance(max_, list):
            max_ = max_[0]

        try:
            self.terms.getTermByToken(min_)
        except LookupError:
            min_ = default

        try:
            self.terms.getTermByToken(max_)
        except LookupError:
            max_ = default

        if min_ == default and max_ == default:
            return default

        if min_ is None and max_ is None:
            return default

        return (min_, max_)


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def ValueRangeFieldWidget(field, request):
    """IFieldWidget factory for ValueRangeWidget."""
    return FieldWidget(field, ValueRangeWidget(request))
