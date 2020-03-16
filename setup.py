
from setuptools import setup, find_packages
from codecs import open
from os import path
import qogir

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

long_description = ''

setup(
    name='qogir',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=qogir.VERSION,

    description='Qogir: Make task easier',
    long_description=long_description,

    # The project's main homepage.
    url='',

    # Author details
    author='Jerevia',
    author_email='trilliondawn@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    # What does your project relate to?
    keywords='qogir spark',

    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'pyyaml',
        'virtualenv',
    ],

    python_requires='>=2.6',

    extras_require={
        'dev': [],
        'test': [],
    },

    entry_points={
        'console_scripts': [
            'qogir = qogir.core:execute_from_command_line',
        ],
    },
)