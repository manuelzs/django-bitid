============
django-bitid
============

A django app for bitId_  authentication.

Installation
============

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

* pybitid
* south: provides migrations
* pytz: for timezone aware date comparisons

*NOTE*: The PyBitID_ project, as this project, is very early stage. Currently it has to be installed manually from:

https://github.com/LaurentMT/pybitid

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
