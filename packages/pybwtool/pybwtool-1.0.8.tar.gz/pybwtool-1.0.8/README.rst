pybwtool
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Python wrapper for the `bwtool library <https://github.com/CRG-Barcelona/bwtool>`_.
Please take a look to the `bwtool wiki <https://github.com/CRG-Barcelona/bwtool/wiki#installation>`_ for notes
on the installation process and to the known issues 
listed below within this readme.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install pybwtool

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes get slightly
different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Extract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The :code:`extract` method returns a tuple of pandas Dataframes
with the data from the regions of a bed file extracted from the given bigwig.

.. code:: python

    from pybwtool import extract

    results = extract(
        bed_path="path/to/my/bed_file.bed",
        bigwig_path="path/to/my/bigwig_file.bigwig"
    )

You can also run the extraction directly to a file,
a thing that can get handy when you have to run
a very big bed file. You just need to specify a target file.

.. code:: python

    from pybwtool import extract

    extract(
        bed_path="path/to/my/bed_file.bed",
        bigwig_path="path/to/my/bigwig_file.bigwig",
        target="target.bed"
    )

It is also possible to directly export
to a compressed file just by adding the
gzip extension, as follows:

.. code:: python

    from pybwtool import extract

    extract(
        bed_path="path/to/my/bed_file.bed",
        bigwig_path="path/to/my/bigwig_file.bigwig",
        target="target.bed.gz"
    )

Common fixes for getting bwtool to work
----------------------------------------------
Consider looking at the Travis-CI configuration.
If it works there, it should also work for you.

- `For when the installation of bwtool gets stuck <https://github.com/CRG-Barcelona/bwtool/issues/65>`_
- `For when the installation of libbeato (a required library) gets stuck <https://github.com/CRG-Barcelona/libbeato/issues/6>`_



.. |travis| image:: https://travis-ci.org/LucaCappelletti94/pybwtool.png
   :target: https://travis-ci.org/LucaCappelletti94/pybwtool
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_pybwtool&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_pybwtool
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_pybwtool&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_pybwtool
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_pybwtool&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_pybwtool
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/pybwtool/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/pybwtool?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/pybwtool.svg
    :target: https://badge.fury.io/py/pybwtool
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/pybwtool
    :target: https://pepy.tech/badge/pybwtool
    :alt: Pypi total project downloads 

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/6f79fce7cb144f509ed584af3f950ab8
    :target: https://www.codacy.com/manual/LucaCappelletti94/pybwtool?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/pybwtool&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/68b5e35660142727406a/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/pybwtool/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/68b5e35660142727406a/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/pybwtool/test_coverage
    :alt: Code Climate Coverate
