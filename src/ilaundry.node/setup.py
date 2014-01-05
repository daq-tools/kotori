from setuptools import setup, find_packages

requires = [
    'twisted==13.2.0',
    'autobahn==0.7.0',
    'appdirs==1.2.0',
]

setup(name='ilaundry.node',
      version='0.0.1',
      description='ilaundry.node',
      long_description='iLaundry node service',
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
      test_suite='ilaundry.test',
      install_requires=requires,
      dependency_links=[
          #'https://github.com/tavendo/AutobahnPython/tarball/cb322f78ffaa2a5#egg=autobahn-0.7.0',
      ],
      entry_points={
          'console_scripts': [
              'ilaundry-node = ilaundry.node.nodeservice:run',
          ],
      },
)
