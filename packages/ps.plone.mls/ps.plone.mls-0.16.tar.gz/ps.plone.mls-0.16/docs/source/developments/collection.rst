======================
Development Collection
======================


Working With Development Collections
====================================


Activate A Development Collection
---------------------------------

To show development projects within your site, go to the place in your Plone site where you want to have the development projects available and open the **Actions**-menu.
Select **Activate Development Collection** from the available options:

.. figure:: ../../_images/development_collection_activate.png

   Activate a development collection

When the **Development Collection** was activated, you will see a status message:

.. figure:: ../../_images/development_collection_activate_done.png

   Confirmation that the development collection has been activated

This will by default show you all available development projects from your connected MLS.

.. figure:: ../../_images/development_collection_default.png

   List of development projects after collection has been activated


Deactivate A Development Collection
-----------------------------------

You can disable the embedding of development projects at any time.
When you deactivate the embedding, your configuration will not be removed.
So if you later decide to enable the embedding again, you don't have to start from the beginning.

To deactivate the **Development Collection**, open the **Actions**-menu and select **Deactivate Development Collection**:

.. figure:: ../../_images/development_collection_deactivate.png

   Deactivate a development collection

When the **Development Collection** was deactivated, you will see a status message:

.. figure:: ../../_images/development_collection_deactivate_done.png

   Confirmation that the development collection has been deactivated


Configuration Options
=====================

To change the settings for this embedding, click on the link **Configure Development Collection**.

The configuration is split into two parts:

- Basic Settings (define the representation of the developments)
- Filter Options (set pre-defined search criterias)


Basic Settings
--------------

With the basic settings, available under the **Default** tab, you can adjust the visual representations of the developments:

.. figure:: ../../_images/development_collection_configuration.png

   Basic configuration options for a development collection

Zoom level for maps
    This is the default level of detail for the maps within the community page of a development.
    You can choose a value between *0* and *21*, where *0* shows the entire world and *21* is at street level.
    Please note that not all zoom levels are available for all areas.

Show Banner Image
    Enable this setting to show a development banner in the collection.

Show Contact Information
    Enable this setting to show the contact information for this development.
    If the **customized contact information** is enabled (either globally in the Plone site or locally for your embedding), the contact information will be updated or replaced based on those settings.

Show Contact Form
    Enable this setting to show a contact form within the community page of a development.
    When the contact form is submitted, an email will be sent to the responsible agent about that request.
    If the **customized contact information** is enabled (either globally in the Plone site or locally for your embedding), the email will be sent to the therein set email address of the responsible agent.

Alternative Email recipient
    Adjust the recipient for the email sent from the contact form.
    By default the responsible agent will receive the email.

BCC Recipients
    Add additional email addresses (comma separated) which should a receive a copy of the contact form.

Show Contact-Us anchor link
    Enable this setting to show an link to the contact form on the top of the page.

Show Captcha
    Enable this setting to show a spam preventing captcha within the contact form.

Modify URLs
    Enable this setting to add extra information to the generated URLs, like title and location.

Developments per Page
    How many developments should be visible per page?
    If more developments are available, users can use the provided links to navigate through the search results.

Listings per Page
    How many listings should be visible per devlopment listings page?
    If more listings are available, users can use the provided links to navigate through the search results.


Filter Options
--------------

To refine the search results for the develoments, use the options provided at the **Filter Options** tab:

.. figure:: ../../_images/development_collection_configuration_filter.png

   Filter options for a development collection

Agency Developments
    Enable this option to only show developments from the configured agency.

    .. note::
        This filter does not work if the agency ID set in the MLS configuration does not match the provided API key.

Searchable Text
    Use this option to search for developments.
    The information which is used for this search criterium is based on the following information of a development project:

    - **id**: The ID of the development, as shown in the URL of the browser address bar, like ``cayo-ranch``.
    - **title**: The name/title of the development, like ``Cayo Ranch``.
    - **description**: The short description (available in one or more languages).
    - **long_description**: The detailled description (available in one or more languages).
    - **area_description**: Information about the area (available in one or more languages).
    - **city**: Name of the city, like ``Puerto Cayo``.
    - **district**: Name of the local district (3rd administrative level), like ``Puerto De Cayo``.
    - **region**: Name of the county/region (2nd administrative level), like ``Jipijapa``.
    - **subdivision**: Name of the state/subdivision (1st administrative level), like ``Manabí``.
    - **country**: Name of the county, like ``Ecuador``.

    You can use **AND**, **OR** and **NOT** to build a more complex search query, e.g.::

        ecuador AND NOT quito AND luxury

    Summarizing the default operator rules:

    - A sequence of words without operators implies AND, e.g. ``casa beach``.
    - Double-quoted text implies phrase search, e.g. ``"casa beach"``.
    - Words connected by punctuation implies phrase search, e.g. ``casa-beach``.
    - A leading hyphen implies NOT, e.g. ``casa -beach``
    - These rules can be combined, e.g. ``casa -"casa beach"`` or ``casa -casa-beach``.
    - \* and ? are used for globbing (i.e. prefix search), e.g. ``casa*``.

Sort results by
    Sort the search results by the given sort option.
    The current available values are:

    - **No selection**: The results are sorted by relevance.
    - **Created**: The results are sorted by the date and time the developments were created.
    - **Title**: The results are sorted by the development title.

Reverse sort order?
    Enable this setting to reverse the sort order.

    .. hint::

        To build e.g. a *Recent Developments* collection, where the newest developments will show up first, select **Created** from the **Sort results by** selection and enable the **Reverse sort order?** option.

Once all configuration options are entered click the **Save** button.


Available Layouts
=================

Developments As Rows
--------------------

The collection results by default show as rows:

.. figure:: ../../_images/development_collection_default.png

   Development collection results as rows.


Developments As Rows With Development Banner
--------------------------------------------

If the *Show Banner Image* option is selected, the collection results will show the development project banner too:

.. figure:: ../../_images/development_collection_with_banner.png

   Development collection results as rows with development project banner.
