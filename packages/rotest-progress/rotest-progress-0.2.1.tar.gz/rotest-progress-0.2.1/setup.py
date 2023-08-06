"""Handling packaging and distribution of this package."""
from __future__ import absolute_import
from setuptools import setup


setup(
    name='rotest-progress',
    version="0.2.1",
    description="Adds a progress bar based on remote statistics where it can",
    long_description=open("README.rst").read(),
    license="MIT",
    author="gregoil",
    author_email="gregoil@walla.co.il",
    url="https://github.com/gregoil/rotest-progress",
    keywords="rotest testing system django unittest progress",
    install_requires=[
        'rotest',
        'tqdm',
        'tkscrolledframe',
    ],
    extras_require={
        "dev": [
            "flake8",
            "pylint",
        ]
    },
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    entry_points={
        "rotest.result_handlers": [
            "progress = "
            "rotest_progress:CurrentProgressHandler",
            "full_progress = "
            "rotest_progress:FullProgressHandler",
            "tk_progress = "
            "rotest_progress:TkinterProgressHandler",
        ],
    },
    packages=['rotest_progress'],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)
