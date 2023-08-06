validate_version_code
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package to validate version codes.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install validate_version_code

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage example
--------------------------------------------
He's a basic how to:

.. code:: python

    from validate_version_code import validate_version_code

    valid_version_code = "1.2.3"
    invalid_version_code = "beta.3"

    assert validate_version_code(valid_version_code)
    assert not validate_version_code(invalid_version_code)

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/validate_version_code.png
   :target: https://travis-ci.org/LucaCappelletti94/validate_version_code
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_validate_version_code&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_validate_version_code
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_validate_version_code&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_validate_version_code
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_validate_version_code&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_validate_version_code
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/validate_version_code/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/validate_version_code?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/validate_version_code.svg
    :target: https://badge.fury.io/py/validate_version_code
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/validate_version_code
    :target: https://pepy.tech/badge/validate_version_code
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/7a1b6189d2b740319aee86fd8a7cecf4
    :target: https://www.codacy.com/app/LucaCappelletti94/validate_version_code?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/validate_version_code&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/4edd0e56c8b989a77b7c/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/validate_version_code/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/4edd0e56c8b989a77b7c/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/validate_version_code/test_coverage
    :alt: Code Climate Coverate