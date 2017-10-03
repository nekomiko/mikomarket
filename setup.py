from setuptools import setup

setup(
    name='mikomarket',
    packages=['mikomarket'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'lxml',
        'requests',
    ],
)
