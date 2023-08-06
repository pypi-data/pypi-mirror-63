# BenBot
Python wrapper for BenBot.

[![Requires: Python 3.x](https://img.shields.io/pypi/pyversions/BenBot.svg)](https://pypi.org/project/BenBot/)
[![BenBot Version: 1.0.1](https://img.shields.io/pypi/v/BenBot.svg)](https://pypi.org/project/BenBot/)

## Installing:
### Synchronous:
Windows: ``py -3 -m pip install BenBot``<br>
Linux/macOS: ``python3 -m pip install BenBot``

### Asynchronous:
Windows: ``py -3 -m pip install AsyncBenBot``<br>
Linux/macOS: ``python3 -m pip install AsyncBenBot``

## Examples:
```
import BenBotAsync
import asyncio

async def ben_search():
    result = await BenBotAsync.get_cosmetic(
        "Ghoul Trooper",
        params=BenBotAsync.Tags.NAME,
        filter=[BenBotAsync.Filters.TYPE, 'Outfit']
    )

    print(result.id)

loop = asyncio.get_event_loop()
loop.run_until_complete(ben_search())
loop.close()
```

This would output:<br>
```CID_029_Athena_Commando_F_Halloween```

fortnitepy example:
```
import fortnitepy
import BenBotAsync

client = fortnitepy.Client(
    email='example@email.com',
    password='password123'
)

@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    content = " ".join(split)

    if args[0] == '!skin':
        skin = result = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Outfit']
        )

        await client.user.party.me.set_outfit(asset=skin.id)

client.run()
```

The list of functions is on the Wiki.
