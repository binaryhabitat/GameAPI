# GameAPI
A wrapper for popular Game APIs - ``pip install GameAPI``.

#### Supported Games
- Blizzard
    - Diablo 3
    - Hearthstone
    - World of Warcraft
    - World of Warcraft Classic

## Examples
#### Blizzard
In order to generate your own _client_id_ and _client_secret_ please visit [https://develop.battle.net/access/](https://develop.battle.net/access/).
```Python3
from GameAPI.blizzard import BlizzardAPI

# Setup the API
api = BlizzardAPI(client_id="Example", client_secret="Example", region="EU")

# Retrieve the current WoW Token price
result = api.wow.token()

# Retrieve the achievements for Kungen on Tarren Mill.
result = api.wow.character_achievements_summary("tarren-mill", "kungen")

# Retrieve all Eras in Diablo 3
result = api.diablo3.era_index()

# Search for a Hearthstone Card
result = api.hearthstone.card_search(health=4, attack=1)
```

### Credits
The original inspiration for creating GameAPI came from [python-wowapi](https://github.com/lockwooddev/python-wowapi), 
as during Summer 2020 Blizzard radically altered the API endpoints, python-wowapi was slow to update and while I cannot
criticise a freely distributed project, it did necessitate in the creation of this library. 
python-wowapi is/was maintained by [lockwooddev](https://github.com/lockwooddev).

Unbeknownst to myself, a contributor ([trevorphillipscoding](https://github.com/trevorphillipscoding))
on python-wowapi developed a separate fork, named [python-blizzardapi](https://github.com/trevorphillipscoding/python-blizzardapi). 
GameAPI makes absolutely no use of code from either project, the latter only being discovered while doing due diligence before publishing to PyPi. 
However, it is correct and proper both of these projects are given a mention. If GameAPI doesn't satisfy your needs,
I direct you in their direction to see if their projects satisfy your needs.

### The Legal Stuff
#### Blizzard Entertainment
- The Blizzard API Terms of Use can be found [here](https://www.blizzard.com/en-us/legal/a2989b50-5f16-43b1-abec-2ae17cc09dd6/blizzard-developer-api-terms-of-use).
- All data is sourced by official Blizzard Entertainment APIs.
- Blizzard Entertainment does not endorse this project, or projects that use this library.
- All trademarks are owned by their respective owners - primarily BLIZZARD ENTERTAINMENT, INC.

