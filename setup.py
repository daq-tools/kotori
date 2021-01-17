# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [

    # Core
    'Twisted[tls]==20.3.0',
    'pyOpenSSL>=16.2.0',
    'six>=1.15.0',
    'pyramid==1.9.4',
    'pyramid_jinja2>=2.8,<3',
    'cornice>=5.0.3,<6',
    'simplejson>=3.17.2,<4',
    'Jinja2>=2.11.2,<3',
    'Bunch>=1.0.1,<2',
    'munch>=2.5.0,<3',
    'appdirs>=1.4.3,<2',
    'json-store>=3.0,<4',
    'python-dateutil>=2.8.0,<3',
    'arrow>=0.17.0,<1',
    'funcy>=1.15,<2',
    'attrs>=20.2.0,<21',

    # Bus adapters
    'paho-mqtt>=1.5.1,<2',
    'autobahn[twisted]>=20.7.1,<21',
    'msgpack-python>=0.5.6,<0.6',
    'PyTrie>=0.4.0,<1',

    # Misc
    'distlib>=0.3.1,<0.4',
    'docopt>=0.6.2,<0.7',

    # More dependencies
    'cryptography>=3.1.1',
    'certifi>=2020.6.20',

    'service_identity>=18.1.0,<19',
    'idna>=2.10,<3',
    'pyasn1>=0.4.8,<0.5',
    'pyasn1-modules>=0.2.8,<0.3',

]

extras = {
    'daq': [
        'influxdb>=5.3.0,<6',
        'pytz>=2020.1',
        'requests>=2.12.4,<3',
        'grafana_api_client==0.2.0',
        #'grafana-dashboard-builder==0.1.0a7',      # evaluated, but not suitable
        #'txmongo==16.3.0',
        'pymongo>=3.11.0,<4',
    ],
    'daq_geospatial': [
        'Geohash>=1.0,<2',
        'geopy>=1.12.0,<2',
        'Beaker>=1.9.0,<2',
        'tqdm>=4.19.8,<5',
    ],
    'daq_binary': [
        'pycparser==2.17',          # 2.18
        'pyparsing==2.2.0',
        'pyclibrary==0.1.3',
        'tabulate==0.7.5',          # 0.8.2
        'sympy==0.7.6.1',           # 1.1.1
    ],
    'storage_plus': [
        'alchimia>=0.4,<1',
    ],

    # Data export: Basic formats
    'export': [
        'pyinfluxql==0.0.1',
        'pandas>=1.1.5,<1.3',
        'numpy>=1.19.2,<1.20',
        'XlsxWriter>=1.3.6,<1.4',
    ],

    'plotting': [
        #'dyplot==0.8.8',

        # sudo port install py27-matplotlib
        'matplotlib>=3.3.2,<3.4',
        #'cairocffi>=0.5.4',
        'bokeh>=2.2.2,<2.3',
        'vincent>=0.4.4,<0.5',
    ],

    # Data export: Scientific data formats like HDF5 and NetCDF and plots from ggplot
    'scientific': [

        # Data
        # ----
        # HDF5
        # "PyTables" requires HDF5 libraries
        # sudo port install hdf5
        'tables>=3.6.1,<3.7',
        'h5py>=2.10.0,<4',

        # NetCDF (Network Common Data Form)
        'xarray>=0.16.1,<0.17',
        # sudo port install netcdf
        'netCDF4>=1.5.4,<1.6',
        #'h5netcdf==0.2.2',

        # Algorithms
        # ----------
        # sudo port install py27-scipy
        'scipy>=1.5.3,<1.6',
        'ggplot>=0.11.5,<0.12',

        # gfortran
        # aptitude install libatlas-base-dev lapack-dev gfortran or
        # https://gcc.gnu.org/wiki/GFortranBinaries

        # Visualization
        # -------------
        #'seaborn==0.7.1',

    ],

    'firmware': [
        'GitPython>=2.0.5,<3',
        'plumbum>=1.6.1,<1.7',
    ],

}

setup(name='kotori',
      version='0.25.0',
      description='Kotori is a data acquisition, processing and graphing toolkit for humans',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: System :: Archiving",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='Andreas Motl',
      author_email='andreas.motl@getkotori.org',
      url='https://github.com/daq-tools/kotori',
      keywords='data acquisition graphing export plotting daq routing engine ' +
               'mqtt http rest amqp wamp sql web html csv json cdf hdf5 png ' +
               'twisted pyramid autobahn influxdb mosquitto grafana mongodb matplotlib ggplot ' +
               'telemetry m2m iot',
      packages=find_packages(),
      include_package_data=True,
      package_data={
        'kotori': [
          'daq/graphing/grafana/resources/*.json',
          'io/export/*.html',
        ],
      },
      zip_safe=False,
      test_suite='kotori.test',
      install_requires=requires,
      extras_require=extras,
      dependency_links=[
          'https://github.com/jjmalina/pyinfluxql/tarball/d92db4ab8c#egg=pyinfluxql-0.0.1',
      ],
      entry_points={
          'console_scripts': [
              'kotori              = kotori:run',
              #'kotori-master      = kotori.master.server:run',
              #'kotori-node        = kotori.node.nodeservice:run',
              #'kotori-wamp-client = kotori.master.client:run_wamp_client',
              'h2m-csv-udp-client  = kotori.vendor.hydro2motion.client:run_udp_client',
              'h2m-csv-udp-fuzzer  = kotori.vendor.hydro2motion.client:run_udp_fuzzer',
              'lst-message         = kotori.vendor.lst.shell:message',
              'kotori-selftest     = kotori.vendor.selftest:run',
          ],
          'paste.app_factory': [
              'main = kotori.frontend.app:main',
          ],
      },
)
