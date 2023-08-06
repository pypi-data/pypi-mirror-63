
import io
import re
import setuptools
import sys

with io.open('src/nr/parsing/date.py', encoding='utf8') as fp:
  version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

with io.open('README.md', encoding='utf8') as fp:
  long_description = fp.read()

requirements = []
extras_require = {}
extras_require['test'] = ['python-dateutil']
tests_require = []
tests_require = ['python-dateutil']

setuptools.setup(
  name = 'nr.parsing.date',
  version = version,
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  description = 'A simple and fast date parsing library. Uses dateutil for timezone offset support.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://git.niklasrosenstein.com/NiklasRosenstein/nr-python-libs',
  license = 'MIT',
  packages = setuptools.find_packages('src', ['test', 'test.*', 'docs', 'docs.*']),
  package_dir = {'': 'src'},
  include_package_data = False,
  install_requires = requirements,
  extras_require = extras_require,
  tests_require = tests_require,
  python_requires = None, # TODO: '>=2.7,<3.0.0|>=3.4,<4.0.0',
  data_files = [],
  entry_points = {},
  cmdclass = {},
  keywords = [],
  classifiers = [],
)
