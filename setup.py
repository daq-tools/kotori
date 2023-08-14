# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from versioningit import get_cmdclasses

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='kotori',
      cmdclass=get_cmdclasses(),
      description='Kotori is a data acquisition, processing and graphing toolkit for humans',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      python_requires='>=3.5',
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
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
               'telemetry m2m iot sensor-network sensorwan',
      packages=find_packages(include=["kotori*"], exclude=["tasks", "test"]),
      include_package_data=True,
      package_data={
        'kotori': [
          'daq/graphing/grafana/resources/*.json',
          'io/export/*.html',
          'frontend/templates/*.html',
        ],
      },
      zip_safe=False,
      install_requires=[

        # Core
        'Twisted[tls]<26',
        'pyOpenSSL>=16.2.0',
        'setuptools<81',
        'six>=1.15.0',
        'pyramid<1.11',
        'pyramid_jinja2>=2.8,<3',
        'cornice>=5.0.3,<7',
        'simplejson>=3.17.2,<4',
        'Jinja2<4',
        'munch>=2.5.0,<5',
        'appdirs>=1.4.3,<2',
        'json-store>=3.1,<5',
        'python-dateutil>=2.8.0,<3',
        'arrow>=0.17.0,<2',
        'funcy>=1.15,<3',
        'attrs>=20.2.0,<26',
        "importlib-metadata; python_version<'3.8'",

        # Bus adapters
        'paho-mqtt>=1.5.1,<3',
        'autobahn[twisted]>=20.7.1,<26',
        'msgpack-python>=0.5.6,<0.6',
        'PyTrie>=0.4.0,<1',

        # Misc
        'distlib<0.5',
        'docopt-ng<0.10',

        # More dependencies
        'cryptography>=2.9.2',
        'certifi>=2020.6.20',

        'service_identity<25',
        'idna<4',
        'pyasn1<0.7',
        'pyasn1-modules<0.5',
      ],
      extras_require={

        'full': ['kotori[daq,daq_geospatial,export,scientific,firmware]'],

        'daq': [
            'influxdb>=5.3.0,<6',
            'pytz>=2020.1',
            'requests>=2.12.4,<3',
            'grafana_api_client==0.2.0',
            #'grafana-dashboard-builder==0.1.0a7',      # evaluated, but not suitable
            #'txmongo==16.3.0',
            'pymongo>=3.11.0,<5',
        ],
        'daq_geospatial': [
            'Geohash>=1.0,<2',
            'geopy>=1.12.0,<3',
            'Beaker>=1.9.0,<2',
            'tqdm<5',
        ],
        'daq_binary': [
            'pycparser<3.1',
            'pyparsing<3.4',
            'pyclibrary<0.4',
            'tabulate<0.8',
            'sympy<1.15',
        ],
        'storage_plus': [
            'alchimia>=0.4,<1',
        ],

        # Data export: Basic formats
        'export': [
            'pyinfluxql>=0.0.1,<1',
            'numpy==1.18.5; python_version=="3.5"',
            'pandas<1.3; python_version<"3.10"',
            'numpy<1.22; python_version<"3.10"',
            'pandas<1.6; python_version<"3.12"',
            'numpy<1.25; python_version<"3.12"',
            'pandas<3; python_version<"3.13"',
            'numpy<2; python_version<"3.13"',
            'pandas<4',
            'numpy<3',
            'XlsxWriter>=1.3.6,<4',
        ],

        'plotting': [
            #'dyplot==0.8.8',

            'matplotlib>=3,<3.11',
            'plotnine<0.13',
            #'cairocffi>=0.5.4',
        ],

        # Data export: Scientific data formats like HDF5 and NetCDF and plots from ggplot
        'scientific': [

            # Data
            # ----

            # "PyTables" requires HDF5 libraries.
            "h5py>=2.10.0,<4; python_version<'3.11'",
            "tables>=3.5.2,<4; python_version<'3.11'",

            # NetCDF (Network Common Data Form)
            'xarray<2025',
            'netCDF4>=1.5.3,<1.8',
            #'h5netcdf==0.2.2',

            # Algorithms
            # ----------
            #'scipy>=1.4.1,<1.6',

            # gfortran
            # aptitude install libatlas-base-dev lapack-dev gfortran or
            # https://gcc.gnu.org/wiki/GFortranBinaries

            # Visualization
            # -------------
            'bokeh>=1.4.0,<4',
            #'seaborn==0.7.1',
            'vincent>=0.4.4,<0.5',

        ],

        'firmware': [
            'GitPython>=2.0.5,<4',
            'plumbum>=1.6.1,<1.11',
        ],

        # Development.
        'test': [
            'pytest<8',
            'pytest-cov<8',
            'pytest-twisted<2',
            'datadiff<3',
            'coverage<8',
        ],
        'release': [
            'build',
            'bump2version<2',
            'twine<7',
            'keyring<26',
            'invoke<3',
            'requests<3',
            'sh<3',
        ],
      },
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
