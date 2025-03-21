#!/usr/bin/env python
from setuptools import find_packages, setup


project = "app-ddog-metric"
version = "1.0.0"

setup(
    # name=project,
    version=version,
    description="Get OPP DB row count and write metric to Datadog",
    author="Test User 101",
    author_email="engineering@testuser101.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click>=8.0.3',
        'datadog>=0.42.0',
        'requests>=2.26.0',
        'simplejson>=3.17.5'
    ],
    entry_points={
        'console_scripts': [
            'app-ddog-metric = app_ddog_metrics.main:cli'
        ],
    },
    extras_require={
        "test": [
            "nose>=1.3.7",
            "PyHamcrest>=1.9.0",
            "coverage>=5.0.4"
        ],
        "lint": [
            "isort>=5.10.1",
            "flake8>=4.0.1"
        ],
    }
)
