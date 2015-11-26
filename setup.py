from setuptools import setup, find_packages

requires = [
    'setuptools>=18.3.1',   # setuptools>=18.3.1 is required by set(['crossbar'])
    'pyasn1==0.1.9',        # required by service-identity
    'Twisted==15.4.0',
    'autobahn==0.10.9',
    'crossbar==0.11.1',
    'appdirs==1.4.0',
    'docopt==0.6.2',
    'json-store==2.1',
    'alchimia==0.4',    # 0.6.1
    'txmongo==0.6',     # 15.2.2
    'influxdb==2.10.0',
    'pyramid==1.5.7',
    'pyramid_jinja2==2.5',
    'cornice==1.0.0',
    'twisted-mqtt==0.1.2',
    'Bunch==1.0.1',
    'grafana_api_client==0.1.4',
    #'grafana-dashboard-builder==0.1.0a7',
    'Jinja2==2.8',
    'pyclibrary==0.1.2',
    'tabulate==0.7.5',
    'sympy==0.7.6.1',
    'msgpack-python==0.4.6',
]

setup(name='kotori',
      version='0.4.0',
      description='Kotori',
      long_description='Kotori',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Twisted",
        "Topic :: Internet :: WWW/HTTP",
        ],
      author='',
      author_email='',
      url='',
      keywords='web twisted autobahn',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='kotori.test',
      install_requires=requires,
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
