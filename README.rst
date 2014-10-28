============
django-bitid
============

A django app for bitId_  authentication.

WARNING: The bitId_ specification is a work in progress and it will probably change.

Installation
============

From pip:

``pip instal django-bitid``

Set Up
------

In your setting.py file, add the backend to AUTHENTICATION_BACKENDS.

``djbitid.backends.BitIdBackend``

You can implement your own login passing ``bitid_uri``, ``callback_uri``, ``signature`` and ``address`` to the backend or use the provided `templates and forms <#templates-and-forms>`_.

Views, Templates and Forms
--------------------------

To use the provided templates and forms add ``djbitid`` to installed apps.

Then add to your urls

``url(r'^bitid/', include('djbid.urls'))``

The provided templates  extend 'base.html'

Dependencies
------------

* PyBitID_
* south: provides migrations
* pytz: for timezone aware date comparisons


Settings
========

Optional settings are:

BITID_USE_TESTNET
-----------------

Use bitcoin testnet. Defaults to False


BITID_CHALLENGE_EXPIRATION_DELAY
--------------------------------

Challenge expiration time in seconds. Defaults to 600 seconds.


.. _bitId: https://github.com/bitid/bitid
.. _PyBitID: https://github.com/LaurentMT/pybitid
