from setuptools import setup, find_packages

setup(
    name='messaging_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',
        'djangorestframework',
        'drf-nested-routers',
    ],
)
