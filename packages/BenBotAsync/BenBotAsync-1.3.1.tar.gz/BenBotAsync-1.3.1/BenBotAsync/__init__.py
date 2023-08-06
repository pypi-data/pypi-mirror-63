"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019
The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.
Software: fortnitepy-bot
License: Apache 2.0
"""

from typing import Tuple

from .enums import *
from .http import HTTPClient
from .cosmetics import fortniteCosmetic
from .api import API

import aiohttp
import base64
import codecs
import fortnitepy
import traceback
import functools
import asyncio

__name__ = 'BenBotAsync'
__version__ = '1.2.8'
__author__ = 'xMistt'


IOS_TOKEN_TEMPLATE = (b'SnJ5cGJ6ciAlZiwgVid6IG4geWJvb2wgb2JnIHpucXIgb2wga1p2ZmdnL3p2Zmdr'
                      b'Ynl2ISBTYmUgdXJ5YywgeXZmZyBicyBwYnp6bmFxZiBiZSB2cyBsYmggam5hYW4g'
                      b'dWJmZyBsYmhlIGJqYSBvYmcsIHdidmEgZ3VyIHF2ZnBiZXE6IHVnZ2NmOi8vcXZm'
                      b'cGJlcS50dC84dXJORUVPLg==')

BEN_BOT_BASE = 'http://benbotfn.tk:8080/api/cosmetics/'

async def set_default_loadout(client: fortnitepy.Client, config: dict, member: fortnitepy.PartyMember) -> None:
    """Function which can be used with fortnitepy to set the default loadout."""

    party_update_meta = client.user.party  # Saves direct route to the party_update_meta object.
    kairos_profile = member.display_name  # Used to generated iOS token required for mass cosmetic updates.

    unique_ios_token = codecs.decode(
        base64.b64decode(
            IOS_TOKEN_TEMPLATE
        ).decode(), 'rot_13'
    ) % kairos_profile

    # Sends unique iOS kairos token in order for request to be accepted via GraphQL.
    await party_update_meta.send(
        unique_ios_token
    )

    await party_update_meta.me.edit_and_keep(  # Sets default loadout.
        functools.partial(
            party_update_meta.me.set_outfit,
            config['cid']
        ),
        functools.partial(
            party_update_meta.me.set_backpack,
            config['bid']
        ),
        functools.partial(
            party_update_meta.me.set_banner,
            icon=config['banner'],
            color=config['banner_colour'],
            season_level=config['level']
        ),
        functools.partial(
            party_update_meta.me.set_battlepass_info,
            has_purchased=True,
            level=config['bp_tier']
        )
    )

    await asyncio.sleep(1)  # Waits 1 second after submitting iOS token before emoting to avoid rate limits.

    await party_update_meta.me.clear_emote()  # Clears emote to allow the next emote to play.
    await party_update_meta.me.set_emote(asset=config['eid'])  # Plays the emote from config.

    if client.user.display_name != member.display_name:  # Welcomes the member who just joined.
        print(f"[PartyBot] [{time()}] {member.display_name} has joined the lobby.")


async def get_cosmetic(query: str, check: Tuple[Enum, str], params: Enum = Tags.NAME, raw: bool = False):
    """Search cosmetic function which can be used without creating HTTP client."""

    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url=f'{BEN_BOT_BASE}search/multiple',
            params={params.value: query}
        )

        response = await request.json()

    if check is None:
        if raw is True:
            return response
        else:
            try:
                cosmetic = fortniteCosmetic(response[0])
                return cosmetic
            except IndexError:
                return None
    else:
        for result in response:
            if result[f'{check[0].value}'] == check[1]:
                if raw is True:
                    return result
                else:
                    cosmetic = fortniteCosmetic(result)
                    return cosmetic
            else:
                pass


# DEPRECATED FUNCTIONS BELOW.

async def getCosmetic():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getCosmeticId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getCosmeticFromId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


# Gets cosmetic with type Outfit.

async def getSkin():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getSkinId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


# Gets cosmetic with type Harvesting Tool.

async def getPickaxe():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getPickaxeId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


# Gets cosmetic with type Back Bling.

async def getBackpack():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getBackpackId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


# Gets cosmetic with type Glider.

async def getGlider():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getGliderId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


# Gets cosmetic with type Emote.

async def getEmote():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getEmoteId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


# Gets cosmetic with type Pet.

async def getPet():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )


async def getPetId():
    print(
        'This function is now deprecated. Join https://discord.gg/VF4txZr'
        'or view the source code to see the new functions.'
    )
