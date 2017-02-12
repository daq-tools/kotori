# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requires = [

    # Core
    'Twisted==16.0.0',              # 16.2.0
    'pyramid==1.5.7',
    'pyramid_jinja2==2.5',
    'cornice==1.0.0',               # 1.2.1
    'simplejson==3.8.2',
    'Jinja2==2.8',
    'Bunch==1.0.1',
    'appdirs==1.4.0',
    'json-store==2.1',
    'arrow==0.8.0',
    'funcy==1.7.2',

    # Bus adapters
    #'twisted-mqtt==0.1.4',         # 0.2.1
    'paho-mqtt==1.1',
    'autobahn[twisted]==0.13.0',    # 0.14.1
    'msgpack-python==0.4.7',

    # Misc
    'setuptools==22.0.5',           # 20.6.7; setuptools>=18.3.1 is required by set(['crossbar'])
    'docopt==0.6.2',
]

extras = {
    'daq': [
        'influxdb==2.12.0',
        'grafana_api_client==0.1.4',
        'requests==2.10.0',
        #'grafana-dashboard-builder==0.1.0a7',      # evaluated, but not suitable
        #'txmongo==16.3.0',
        'pymongo==3.4.0',
    ],
    'daq_binary': [
        'pyclibrary==0.1.3',
        'tabulate==0.7.5',
        'sympy==0.7.6.1',           # 1.0
    ],
    'storage_plus': [
        'alchimia==0.4',    # 0.6.1
    ],

    # Data export: Basic formats
    'export': [
        'pyinfluxql==0.0.1',
        'pandas==0.18.1',
        'numpy>=1.8.2',
        'XlsxWriter==0.9.2',
    ],

    'plotting': [
        #'dyplot==0.8.8',

        # sudo port install py27-matplotlib
        'matplotlib>=1.4.2',
        #'cairocffi>=0.5.4',
        'bokeh==0.11.2',
        'vincent==0.4.4',
    ],

    # Data export: Scientific data formats like HDF5 and NetCDF and plots from ggplot
    'scientific': [

        # Data
        # ----
        # HDF5
        # "PyTables" requires HDF5 libraries
        'tables>=3.1.1',        # sudo port install hdf5

        # NetCDF (Network Common Data Form)
        'xarray==0.7.2',
        'netCDF4==1.2.4',       # sudo port install netcdf
        #'h5netcdf==0.2.2',

        # Algorithms
        # ----------
        # sudo port install py27-scipy
        'scipy>=0.14.0',
        'ggplot==0.9.7',

        # gfortran
        # aptitude install libatlas-base-dev lapack-dev gfortran or
        # https://gcc.gnu.org/wiki/GFortranBinaries

        # Visualization
        # -------------
        #'seaborn==0.7.1',

    ],

    'firmware': [
        'GitPython==2.0.5',
        'plumbum==1.6.1.post0',
    ],

}

setup(name='kotori',
      version='0.11.2',
      description='Kotori data acquisition, routing and graphing toolkit',
      long_description='Kotori data acquisition, routing and graphing toolkit',
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: System :: Archiving",
        "Topic :: System :: Networking :: Monitoring",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='Andreas Motl',
      author_email='andreas.motl@elmyra.de',
      url='https://getkotori.org/',
      keywords='data acquisition graphing export plotting daq routine engine' +
               'mqtt wamp http rest sql web html csv json cdf hdf5 png ' +
               'twisted pyramid autobahn influxdb mosquitto grafana mongodb matplotlib ggplot ',
      packages=find_packages(),
      include_package_data=True,
      package_data={
        'kotori': [
          'daq/graphing/resources/*.*',
        ],
      },
      zip_safe=False,
      test_suite='kotori.test',
      install_requires=requires,
      extras_require=extras,
      dependency_links=[
          #'https://github.com/tavendo/AutobahnPython/tarball/cb322f78ffaa2a5#egg=autobahn-0.11.2',
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
              ],
          'paste.app_factory': [
              'main = kotori.frontend.app:main',
          ],
      },
)
