from setuptools import setup, find_packages

requires = [
    'Twisted==16.0.0',
    'autobahn[twisted]==0.13.0',
    'crossbar==0.13.0',
    'msgpack-python==0.4.7',
    'Jinja2==2.8',
    'pyramid==1.5.7',
    'pyramid_jinja2==2.5',
    'cornice==1.0.0',
    'twisted-mqtt==0.1.4',
    'paho-mqtt==1.1',
    'Bunch==1.0.1',
    'appdirs==1.4.0',
    'json-store==2.1',
    'docopt==0.6.2',
    'setuptools>=18.3.1',   # 20.6.7; setuptools>=18.3.1 is required by set(['crossbar'])
    'pyasn1==0.1.9',        # required by service-identity
    'cryptography>=0.7',
]

extras = {
    'daq': [
        'influxdb==2.12.0',
        'grafana_api_client==0.1.4',
        #'grafana-dashboard-builder==0.1.0a7',      # tested, but not suitable
    ],
    'daq_binary': [
        'pyclibrary==0.1.3',
        'tabulate==0.7.5',
        'sympy==0.7.6.1',           # 1.0
    ],
    'storage_plus': [
        'alchimia==0.4',    # 0.6.1
        'txmongo==0.6',     # 16.0.1
    ],
}

setup(name='kotori',
      version='0.7.0',
      description='Kotori data acquisition and graphing toolkit',
      long_description='Kotori data acquisition and graphing toolkit',
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Framework :: Pyramid",
        "Framework :: Twisted",
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

        ],
      author='Andreas Motl',
      author_email='andreas.motl@elmyra.de',
      url='https://getkotori.org/',
      keywords='daq mqtt wamp http rest sql web twisted pyramid autobahn influxdb mosquitto grafana mongodb',
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
          #'https://github.com/tavendo/AutobahnPython/tarball/cb322f78ffaa2a5#egg=autobahn-0.7.0',
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
