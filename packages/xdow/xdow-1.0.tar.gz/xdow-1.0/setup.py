from setuptools import setup

setup(
    name='xdow',
    version='1.0',
    description='Adult video downloader',
    author='pankaj kumar',
    author_email='pankajthekush@gmail.com',
    packages=['xdow'],
    install_requires=['js2py', 'requests', 'bs4','wheel'],
    entry_points={"console_scripts": ["xdow = xdow.xdow:classifier"]}
)
