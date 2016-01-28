from setuptools import setup, find_packages

requires = [
    'Twisted==15.4.0',
    'cryptography>=0.7',
    'autobahn==0.10.9',
    'crossbar==0.11.1',
    'Jinja2==2.8',
    'pyramid==1.5.7',
    'pyramid_jinja2==2.5',
    'cornice==1.0.0',
    'twisted-mqtt==0.1.2',
    'pyasn1==0.1.9',        # required by service-identity
    'Bunch==1.0.1',
    'appdirs==1.4.0',
    'json-store==2.1',
    'docopt==0.6.2',
    'setuptools>=18.3.1',   # setuptools>=18.3.1 is required by set(['crossbar'])
]

extras = {
    'storage': [
        'alchimia==0.4',    # 0.6.1
        'txmongo==0.6',     # 15.2.2
    ],
    'daq': [
        'influxdb==2.10.0',
        'grafana_api_client==0.1.4',
        #'grafana-dashboard-builder==0.1.0a7',
    ],
    'daq_binary': [
        'pyclibrary==0.1.2',
        'tabulate==0.7.5',
        'sympy==0.7.6.1',
        'msgpack-python==0.4.6',
    ],
}

setup(name='kotori',
      version='0.5.1',
      description='Kotori data acquisition and graphing toolkit',
      long_description='Kotori data acquisition and graphing toolkit',
      classifiers=[
        "Programming Language :: Python",
        "License :: Other/Proprietary License",
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
      url='http://isarengineering.de/docs/kotori/',
      keywords='daq mqtt wamp http rest sql web twisted pyramid autobahn influxdb mosquitto grafana mongodb',
      packages=find_packages(),
      include_package_data=True,
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
