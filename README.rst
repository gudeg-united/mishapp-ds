mishapp-ds
~~~~~~~~~~

.. image:: https://img.shields.io/codeship/b08ec1b0-8dbb-0132-422a-669677a474c3.svg?style=flat-square&label=codeship
    :alt: Codeship status
    :target: https://codeship.com/projects/60754

Disaster Types
==============

* ``earthquake``
* ``tsunami``
* ``cyclone``
* ``flood``

Spiders
=======

Here's a list of available spiders:

* ``bmkg``
* ``gdacs``

Each spider fetches different disaster data. Common items are:

``source``
    Lowercased source name
``source_id``
    Unique string of data ID
``disaster_type``
    Disaster category name (e.g. `earthquake`)
``country``
    Country name where the disaster took place
``lat``
    Latitude string
``lon``
    Longitude string
``date_time``
    Date and time (in UTC) when the disaster took place

Each datum is published to a Redis channel called ``mishapp-datasource``,
so any script which listens to this channel will be able to read the datum.
Please note, the uniqueness of datum should be handled by consumer script.

BMKG Spider
-----------

This spider crawls and scrapes data from http://bmkg.go.id.
An example of datum emitted by this spider:

.. sourcecode:: python

    {
        'country': 'Indonesia',
        'date_time': '2014-11-15T02:31:44+00:00',
        'depth': '48',
        'disaster_type': 'tsunami',
        'lat': '1.95',
        'lon': '126.46',
        'magnitude': '7.3',
        'source': 'bmkg',
        'source_id': '993bb3f8c2bb641f4a58cf8d090206c5'
    }

GDACS Spider
------------

This spider crawls and scrapes data from http://gdacs.org.
An example of datum emitted by this spider:

.. sourcecode:: python

    {
        'country': 'Indonesia',
        'date_time': '2015-02-04T12:56:00+00:00',
        'depth': '588.53',
        'impact': '813467 people within 100km',
        'lat': '-06.16',
        'lon': '112.99',
        'magnitude': '4.6',
        'source': 'gdacs',
        'source_id': '1048014'
    }
