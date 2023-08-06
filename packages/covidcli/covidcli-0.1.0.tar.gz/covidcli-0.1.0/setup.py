# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covidcli']

package_data = \
{'': ['*'], 'covidcli': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

entry_points = \
{'console_scripts': ['covidcli = covidcli.covidcli:main']}

setup_kwargs = {
    'name': 'covidcli',
    'version': '0.1.0',
    'description': 'Covidcli- A CLI For Tracking and Getting Info About Coronavirus Outbreak',
    'long_description': '### Covidcli \n+ A simple CLI for tracking and getting info about Coronavirus Outbreak\n\n\n#### Dependencies\n+ click\n+ pandas\n+ pyfiglet\n+ tabulate\n\n\n\n#### Installation\n```bash\npip install covidcli\n```\n\n### Usage\n#### Show Cases of Coronavirus By confirmed|recovered|deaths|all\n```bash\ncovidcli show confirmed\n```\n\n\n#### Get Latest Cases of Coronavirus\n```bash\ncovidcli get latest\n```\n\n\n#### Get Previous Cases of Coronavirus\n```bash\ncovidcli get previous\n```\n\n#### Fetch and Download Current Dataset\n```bash\ncovidcli get dataset\n```\n\n\n#### Get Status of Cases By Country\n```bash\ncovidcli get "Italy" --cases confirmed \n```\n\n#### Search Info By Country\n```bash\ncovidcli search "Italy" --cases confirmed \n```\nor\n```bash\ncovidcli search "China" \n```\n\n\n#### Credits For Data\n+ https://github.com/CSSEGISandData\n\n#### By \n+ Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n\n\n\n#### NB\n+ Contributions Are Welcomed\n+ Notice a bug, please let us know.\n+ Thanks A lot',
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jcharis/covidcli',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
