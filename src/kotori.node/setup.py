from setuptools import setup, find_packages

requires = [
    'Twisted==15.0.0',
    'autobahn==0.10.1',
    'crossbar==0.10.2',
    'appdirs==1.4.0',
    'docopt==0.6.2',
    'json-store==2.1',
    'alchimia==0.4',
    'txmongo==0.6',
]

setup(name='kotori.node',
      version='0.2.0',
      description='kotori.node',
      long_description='Kotori node service',
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
              'kotori-master = kotori.master.server:run',
              'kotori-node   = kotori.node.nodeservice:run',
              'kotori        = kotori:run',
              'kotori-wamp-client = kotori.master.client:run_wamp_client',
              'kotori-udp-client  = kotori.master.client:run_udp_client',
              ],
      },
)
