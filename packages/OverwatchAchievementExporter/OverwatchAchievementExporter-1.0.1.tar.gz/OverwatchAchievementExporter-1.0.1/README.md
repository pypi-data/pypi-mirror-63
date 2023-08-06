# galaxy_overwatch_achievement_exporter

[![PyPI version](https://badge.fury.io/py/OverwatchAchievementExporter.svg)](https://pypi.org/project/OverwatchAchievementExporter/)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)

Exports achievements of Overwatch to GOG-compatible format

## Feature

This provides a Python API for fetching a user's achievements from their player profile on the Overwatch website.
Note that this requires the user to have a public profile.

It also provides a method to generate the achievement JSON export for GOG:

```shell script
inv update
```

### api_key

`api_key` is the id of the achievement. Blizzard does not directly provide IDs on their website.
That's the reason we're generating an own id from the achievement name, which seems to be the only constant.
The ID is a lowercase name where all special characters are removed.

## Development

Install dependencies:
```shell script
pip install -r requirements/dev.txt
```