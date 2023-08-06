*** Variables ***

# Documentation  Variables specific for Plone 4.2.x.
# See default.robot for all available variables.

# "Listing Collection"
${LISTING_COLLECTION_N_ITEMS}  css=.listing-summary .tileItem:nth-child(3)

# "Recent Listings"
${RECENT_LISTINGS_N_ITEMS}  css=.listing-summary .tileItem:nth-child(3)

# "Listing Search"
${LISTING_SEARCH_FORM}  css=#search-form

# "Development Collection"
${DEVELOPMENT_COLLECTION_CONFIG_TAB_FILTER}  css=#fieldsetlegend-0
${DEVELOPMENT_COLLECTION_N_ITEMS}  css=.development-summary .tileItem:nth-child(3)


# Settings
${CONTACT_INFO_TAB_DEFAULT}  css=#fieldsetlegend-default
${CONTACT_INFO_TAB_AGENCY}  css=#fieldsetlegend-0
${CONTACT_INFO_TAB_AGENT}  css=#fieldsetlegend-1
