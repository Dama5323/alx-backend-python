from setuptools import setup, find_packages

setup(
    name="django-messaging",  # Better to use a unique name
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
    ],
)