# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slackers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1',
 'pyee>=6.0,<7.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'slackers',
    'version': '0.4.3',
    'description': 'Slack webhooks API served by FastAPI',
    'long_description': '# Slackers\n\nSlack webhooks API served by FastAPI\n\n## What is Slackers\nSlackers is a [FastAPI](https://fastapi.tiangolo.com) implementation to handle Slack interactions and events.\nIt serves endpoints to receive [slash commands](https://api.slack.com/interactivity/slash-commands),\n[app actions](https://api.slack.com/interactivity/actions), [interactive components](https://api.slack.com/interactivity/components). \nIt also listens for events sent to the Slack Events API [Slack Events](https://api.slack.com/events-api). \n\n## Installation\nYou can install Slackers with pip\n`$ pip install slackers`\n\n## Configuration\n### `SLACK_SIGNING_SECRET`\nYou must configure the slack signing secret. This will be used to \nverify the incoming requests signature.   \n`$ export SLACK_SIGNING_SECRET=your_slack_signing_secret`\n\n## Example usage\nSlackers will listen for activity from the Events API on `/events`, for\ninteractive components on `/actions` and for slash commands on `/commands`.\nWhen an interaction is received, it will emit an event. You can listen\nfor these events as shown in the following examples.\n\nOn receiving a request, Slackers will emit an event which you can handle yourself.\nSlackers will also respond to Slack with an (empty) http 200 response telling Slack\nall is well received.\n\n### Starting the server\nAs said, Slackers uses the excellent FastAPI to serve it\'s endpoints. Since you\'re here, \nI\'m assuming you know what FastAPI is, but if you don\'t, you can learn all about \nhow that works with [this tutorial](https://fastapi.tiangolo.com/tutorial/). \n\nSlackers offers you a router which you can include in your own FastAPI.\n```python\nfrom fastapi import FastAPI\nfrom slackers.server import router\n\napp = FastAPI()\napp.include_router(router)\n\n# Optionally you can use a prefix\napp.include_router(router, prefix=\'/slack\')\n```\n\n### Events\nOnce your server is running, the events endpoint is setup at `/events`, or if you use\nthe prefix as shown above, on `/slack/events`.\n\n#### Accepting the challenge\nWhen setting up Slack to [send events](https://api.slack.com/events-api#subscribing_to_event_types),\nit will first send a challenge to verify your endpoint. Slackers detects when a challenge is sent.\nYou can simply start our api and Slackers will meet the challenge automatically.\n\n#### Responding to events\nOn receiving an event, Slackers will emit a python event, which you can act upon as shown below.\n```python\nimport logging\nfrom slackers.hooks import events\n\nlog = logging.getLogger(__name__)\n\n@events.on("app_mention")\ndef handle_mention(payload):\n    log.info("App was mentioned.")\n    log.debug(payload)\n```\n\n\n### Actions\nOnce your server is running, the actions endpoint is setup at `/actions`, or if you use\nthe prefix as shown above, on `/slack/actions`.\n\n#### Responding to actions\nOn receiving an action, Slackers will emit a python event, which you can listen for as \nshown below. You can listen for the action type, or more specifically for the action id\nor callback id linked to the action.\n```python\nimport logging\nfrom slackers.hooks import actions\n\nlog = logging.getLogger(__name__)\n\n# Listening for the action type.\n@actions.on("block_actions")\ndef handle_action(payload):\n    log.info("Action started.")\n    log.debug(payload)\n\n# Listen for an action by it\'s action_id\n@actions.on("block_actions:your_action_id")\ndef handle_action_by_id(payload):\n    log.info("Action started.")\n    log.debug(payload)\n\n# Listen for an action by it\'s callback_id\n@actions.on("block_actions:your_callback_id")\ndef handle_action_by_callback_id(payload):\n    log.info(f"Action started.")\n    log.debug(payload)\n```\n\n#### Custom responses\nSlackers tries to be fast to respond to Slack. The events you are listening for with the\nlikes of `@actions.on(...)` are scheduled as an async task in a fire and forget fashion.\nAfter scheduling these events, Slackers will by default return an empty 200 response which\nmight happen before the events are handled.\n\nIn some cases you might want to act on the payload and return a custom response to Slack.\nFor this, you can use the slackers `responder` decorator to define your custom handler\nfunction. This function is then used as a callback instead of returning the default response.\nYou must ensure your custom handler returns a `starlette.responses.Response` or one of it\'s \nsubclasses. You must furthermore ensure that there is only one responder responding to your\nSlack request.\n\nPlease note that the events are also emitted, so you could have both `@actions.on("block_action:xyz")`\nand `@responder("block_action:xyz")`. Just keep in mind that the event emissions are async and are\nnot awaited. In other words, Slackers doesn\'t ensure that the response (whether your custom response\nor the default) is returned before or after the events are emitted.\n\n```python\nfrom starlette.responses import JSONResponse\nfrom slackers.hooks import responder\n\n@responder("block_actions:your_callback_id")\ndef custom_handler(payload):\n    # handle your payload\n    ...\n    return JSONResponse(content={"custom": "Custom Response"})\n```\n\n### Slash commands\nOnce your server is running, the commands endpoint is setup at `/commands`, or if you use\nthe prefix as shown above, on `/slack/commands`. Slackers will emit an event with the name\nof the command, so if your command is `/engage`, you can listen for the event `engage`\n(without the slash)\n\n#### Responding to slash commands\nOn receiving a command, Slackers will emit a python event, which you can listen for as shown below.\n```python\nimport logging\nfrom slackers.hooks import commands\n\nlog = logging.getLogger(__name__)\n\n\n@commands.on("engage")  # responds to "/engage"  \ndef handle_command(payload):\n    log.info("Command received")\n    log.debug(payload)\n```\n\n### Async\nSince events are emitted using pyee\'s Async event emitter, it is possible to define your event handlers\nas async functions. Just keep in mind that errors are in this case emitted on the \'error\' event. \n\n```python\nimport logging\nfrom slackers.hooks import commands\n\nlog = logging.getLogger(__name__)\n\n@commands.on(\'error\')\ndef log_error(exc):\n    log.error(str(exc))\n\n\n@commands.on("engage")  # responds to "/engage"  \nasync def handle_command(payload):\n    ...\n```\n',
    'author': 'Niels van Huijstee',
    'author_email': 'niels@huijs.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uhavin/slackers',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
