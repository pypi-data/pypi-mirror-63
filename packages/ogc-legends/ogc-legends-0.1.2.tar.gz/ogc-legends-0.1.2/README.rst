ogc-legends
===========

| |Version| |Build Status|

A small library to work with OGC legends. 

.. code-block:: python

    import ogc_legends

    url = "https://demo.mapserver.org/cgi-bin/wms?"
    legends = ogc_legends.get_legends(url, "./images")

    for k, v in legends.items():
        print(k, v)

The dictionary structure returned by the ``get_legends`` function is as follows:

.. code-block:: json

    {
        "cities": [
            {
                "file": "./images\\cities_default.png",
                "style": "default"
            }
        ],
        "continents": [
            {
                "file": "./images\\continents_default.png",
                "style": "default"
            }
        ],
        "country_bounds": [
            {
                "file": "./images\\country_bounds_default.png",
                "style": "default"
            }
        ]
    }

.. image:: https://raw.githubusercontent.com/geographika/ogc-legends/master/images/continents_default.png

From the command line:

.. code-block:: console

    python ogc_legends.py "https://demo.mapserver.org/cgi-bin/wms?" "./images"

Other options - don't override if file already exists, and use WMS version 1.1.1:

.. code-block:: console

    python ogc_legends.py "https://demo.mapserver.org/cgi-bin/wms?" "./images" False "1.1.1"

Requirements
------------

* Python 3.6+

Installation
------------

Note installing the ``ogc-legends`` plugin will automatically install the required dependency ``owslib``. 

.. code-block:: console

    pip install ogc-legends

Releases
--------

0.1 (17/03/2020)
++++++++++++++++

+ Initial release

Author
------

* Seth Girvin `@geographika <https://github.com/geographika>`_

.. |Version| image:: https://img.shields.io/pypi/v/ogc-legends.svg
   :target: https://pypi.python.org/pypi/ogc-legends

.. |Build Status| image:: https://travis-ci.org/geographika/ogc-legends.svg?branch=master
   :target: https://travis-ci.org/geographika/ogc-legends
