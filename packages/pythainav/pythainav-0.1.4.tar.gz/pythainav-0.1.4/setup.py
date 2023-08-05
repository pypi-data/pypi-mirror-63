# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythainav', 'pythainav.utils']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=0.7.2,<0.8.0',
 'furl>=2.1,<3.0',
 'fuzzywuzzy[speedup]>=0.17.0,<0.18.0',
 'requests>=2.22,<3.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'pythainav',
    'version': '0.1.4',
    'description': 'a Python interface to pull thai mutual fund NAV',
    'long_description': '# PythaiNAV\n![Language](https://img.shields.io/github/languages/top/CircleOnCircles/pythainav)\n![Start](https://img.shields.io/github/stars/CircleOnCircles/pythainav)\n![Fork](https://img.shields.io/github/forks/CircleOnCircles/pythainav?label=Fork)\n![Watch](https://img.shields.io/github/watchers/CircleOnCircles/pythainav?label=Watch)\n![Issues](https://img.shields.io/github/issues/CircleOnCircles/pythainav)\n![Pull Requests](https://img.shields.io/github/issues-pr/CircleOnCircles/pythainav.svg)\n![Contributors](https://img.shields.io/github/contributors/CircleOnCircles/pythainav.svg)\n\n![Github_workflow_tatus](https://img.shields.io/github/workflow/status/CircleOnCircles/pythainav/Python%20package)\n![lgtm_gred](https://img.shields.io/lgtm/grade/python/github/CircleOnCircles/pythainav)\n![lgtm_alerts](https://img.shields.io/lgtm/alerts/github/CircleOnCircles/pythainav)\n\n\n![cover image](https://github.com/CircleOnCircles/pythainav/raw/master/extra/pythainav.png)\n\n\nทำให้การดึงข้อมูลกองทุนไทยเป็นเรื่องง่าย\n\n> อยากชวนทุกคนมาร่วมพัฒนา ติชม แนะนำ เพื่อให้ทุกคนเข้าถึงข้อมูลการง่ายขึ้น [เริ่มต้นได้ที่นี้](https://github.com/CircleOnCircles/pythainav/issues) หรือเข้ามา Chat ใน [Discord](https://discord.gg/jjuMcKZ) ได้เลย 😊\n\n## Get Started - เริ่มต้นใช้งาน\n\n```bash\n$ pip install pythainav\n```\n\n```python\nimport pythainav as nav\n\nnav.get("KT-PRECIOUS")\n> Nav(value=4.2696, updated=\'20/01/2020\', tags={\'latest\'}, fund=\'KT-PRECIOUS\')\n\nnav.get("TISTECH-A", date="1 week ago")\n> Nav(value=12.9976, updated=\'14/01/2020\', tags={}, fund=\'TISTECH-A\')\n\nnav.get_all("TISTECH-A")\n> [Nav(value=12.9976, updated=\'21/01/2020\', tags={}, fund=\'TISTECH-A\'), Nav(value=12.9002, updated=\'20/01/2020\', tags={}, fund=\'TISTECH-A\'), ...]\n\nnav.get_all("KT-PRECIOUS", asDataFrame=True)\n> pd.DataFrame [2121 rows x 4 columns]\n```\n\n## Source of Data - ที่มาข้อมูล\n\nดูจาก <https://pythainav.nutchanon.org/datasource/>\n\n## Disclaimer\n\nเราไม่รับประกันความเสียหายใดๆทั้งสิ้นที่เกิดจาก แหล่งข้อมูล, library, source code,sample code, documentation, library dependencies และอื่นๆ\n',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': 'Nutchanon Ninyawee',
    'maintainer_email': 'me@nutchanon.org',
    'url': 'https://github.com/CircleOnCircles/pythainav',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
