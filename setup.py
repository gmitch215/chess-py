from setuptools import setup

setup(
    name='cl-chess',
    packages=['src'],
    version='1.3.0',
    description='A program to play chess on the command line',
    author='Gregory Mitchell',
    author_email='marcusbuffett@me.com',
    url='https://github.com/gmitch215/chess-py',
    entry_points={'console_scripts': ['chess = src.main:main']},
    install_requires=['colored'],
    keywords=['chess', 'game'],
    classifiers=['Programming Language :: Python :: 3'],
)
