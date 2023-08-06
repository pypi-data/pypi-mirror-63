# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitsio']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses_json>=0.4.2,<0.5.0',
 'marshmallow>=3.5.1,<4.0.0',
 'matplotlib>=3.2.0,<4.0.0',
 'pandas>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'splitsio',
    'version': '0.1.1',
    'description': 'A Python implementation of the splits.io REST API.',
    'long_description': "# `splitsio`\n\nA Python implementation of the [`splits.io`](https://splits.io) [REST API](https://github.com/glacials/splits-io/blob/master/docs/api.md).\n\n`splitsio` currently supports read-only access. To upload runs, use the REST API directly.\n\nRequires Python 3.7 or greater.\n\nTo install: `pip3 install splitsio`\n\nThen to access the main data types in Python:\n\n`from splitsio import *`\n\n## Usage\n\n### Game\n\n#### Get information about a game\n\n```python\n>>> sms = Game.from_id('sms')\n>>> sms\nGame(id='15', name='Super Mario Sunshine', shortname='sms')\n>>> sms.created_at\n'2014-04-18T06:28:59.764Z'\n```\n\nNOTE: for games, the identifier for querying is the `shortname` (here `'sms'`), *not* the numerical `id`.\n\n#### Get all games in the database\n\n```python\n>>> games = Game.all()  # this can take a minute or so\n>>> len(games)\n17237\n>>> games[0]\nGame(id='2206', name='007: Agent Under Fire', shortname='auf')\n```\n\n#### Search games by name/keyword\n\n```python\n>>> mario_games = Game.search('mario')\n>>> len(mario_games)\n353\n>>> mario_games[0]\nGame(id='2524', name='Super Mario Advance 4: Super Mario Bros. 3', shortname='sma4')\n```\n\n### Category\n\n#### Get the speedrun categories for a game\n\n```python\n>>> oot = Game.from_id('oot')\n>>> oot.categories[0]\nCategory(id='86832', name='No ACE')\n```\n\n#### Get category from id\n\n```python\n>>> no_ace = Category.from_id('86832')\n>>> no_ace\nCategory(id='86832', name='No ACE')\n```\n\n### Runner\n\n#### Get runners for a game or category\n\n```python\n>>> oot_runners = Game.from_id('oot').runners()\n>>> len(oot_runners)\n238\n>>> oot_runners[0]\nRunner(id='35', twitch_id='31809791', twitch_name='cma2819', display_name='cma2819', name='cma2819')\n>>> no_ace_runners = Category.from_id('86832').runners()\n>>> no_ace_runners[0]\nRunner(id='32189', twitch_id='63370787', twitch_name='bigmikey_', display_name='bigmikey_', name='bigmikey_')\n```\n\n#### Get runner from id\n\n```python\n>>> bigmikey = Runner.from_id('bigmikey_')\n>>> bigmikey\nRunner(id='32189', twitch_id='63370787', twitch_name='bigmikey_', display_name='bigmikey_', name='bigmikey_')\n```\n\nNOTE: for runners, the identifier for querying is the `name` all lowercased (here `'bigmikey_'`), *not* the numerical `id`.\n\n### Run\n\n#### Get runs for a game, category, or runner\n\n```python\n>>> oot_runs = Game.from_id('oot').runs()\n>>> run = oot_runs[0]\n>>> run.realtime_duration_ms\n1507300\n>>> run.program\n'livesplit'\n>>> run.attempts\n97\n>>> len(Category.from_id('86832').runs())\n11\n>>> len(Runner.from_id('bigmikey_').runs())\n2\n```\n\n#### Get attempt histories for a run and its segments\n\n```python\n>>> run = Game.from_id('oot').runs()[0]\n>>> run = Run.from_id(run.id, historic = True)\n>>> len(run.histories)\n90\n>>> run.histories[1]\nHistory(attempt_number=89, realtime_duration_ms=1507300, gametime_duration_ms=None, started_at='2020-03-10T20:06:08.000Z', ended_at='2020-03-10T20:31:15.000Z')\n>>> run.segments[0].name\n'Sword Get'\n>>> len(run.segments[0].histories)\n67\n>>> run.segments[0].histories[0]\nHistory(attempt_number=2, realtime_duration_ms=271832, gametime_duration_ms=0, started_at=None, ended_at=None)\n```\n",
    'author': 'Jeremy Silver',
    'author_email': 'jeremyag@comcast.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeremander/splitsio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
