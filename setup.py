#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

setup(
    author="Howard Medeiros (howard.medeiros@gmail.com)",
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A package to facilitate integration with chatgpt",
    install_requires=[
        "certifi==2022.12.7",
        "charset-normalizer==3.1.0",
        "idna==3.4",
        "requests==2.28.2",
        "urllib3==1.26.15",
    ],
    include_package_data=True,
    keywords='chatgptonic',
    name='chatgptonic',
    packages=find_packages(include=['chatgptonic',
                                    'chatgptonic.*']),
    test_suite='tests',
    url='https://github.com/how-dev/chatgpython',
    version='1.0.0',
    zip_safe=False,
)
