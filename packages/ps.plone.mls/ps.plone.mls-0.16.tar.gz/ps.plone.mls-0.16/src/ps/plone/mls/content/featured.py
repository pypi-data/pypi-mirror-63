# -*- coding: utf-8 -*-
"""Featured Listings."""

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from ps.plone.mls import _
from ps.plone.mls import interfaces
from ps.plone.mls import PLONE_4
from zope import schema
from zope.interface import implementer


if PLONE_4:
    from plone.app.textfield.widget import RichTextFieldWidget


class IFeaturedListings(model.Schema):
    """A list of featured MLS Listings."""

    listing_ids = schema.List(
        description=_(
            u'Add one Listing ID per line for each entry to show up.',
        ),
        title=_(u'MLS Listing IDs'),
        unique=True,
        value_type=schema.TextLine(
            title=_(u'ID'),
        ),
    )

    if PLONE_4:
        directives.widget(body_text=RichTextFieldWidget)
    body_text = RichText(
        required=False,
        title=_('Body Text'),
    )


@implementer(
    IFeaturedListings,
    interfaces.IListingTraversable,
)
class FeaturedListings(Item):
    """A list of featured MLS Listings."""
