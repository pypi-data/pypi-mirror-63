livesplit-id-normalizer
==============

.. image:: https://badge.fury.io/py/livesplit-id-normalizer.png
    :target: https://badge.fury.io/py/livesplit-id-normalizer

.. image:: https://travis-ci.org/narfman0/livesplit-id-normalizer.png?branch=master
    :target: https://travis-ci.org/narfman0/livesplit-id-normalizer

Livesplit split file ids can get out of whack upon manual edit, normalize to
start from 1

Note: this is used for a pretty specific purpose :) if your livesplit ids have
been manually modified to start from a later time, one may use this tool to
basically subtract each id to bring it down to start from 1.

Use case: a runner downloads splits from someone else from splits.io. They
clear out splits using the interface, however, runs for whatever reason still
continue from where the old runs left off. Upon reupload to livesplit, their
runs bizarrely start from wherever the last user left off and gives an odd
user experience.

Installation
------------

Install via pip::

    pip install livesplit-id-normalizer

Development
-----------

Run test suite to ensure everything works::

    make test

Release
-------

To publish your plugin to pypi, sdist and wheels are registered, created and uploaded with::

    make release-test

For test. After ensuring the package works, run the prod target and win::

    make release-prod

License
-------

Copyright (c) 2020 Jon Robison

See LICENSE for details
