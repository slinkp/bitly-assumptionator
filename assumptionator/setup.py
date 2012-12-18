import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, '..', 'README.md')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'requests',
    'simplejson',
    ]

setup(name='assumptionator',
      version='0.0',
      description='assumptionator',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="assumptionator",
      entry_points="""\
      [paste.app_factory]
      main = assumptionator:main
      """,
      )
