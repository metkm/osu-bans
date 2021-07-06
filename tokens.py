from aiohttp import ClientSession
import os
import logging


async def refresh_tokens(tokens: dict) -> dict:
    async with ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data={
            "client_id": 5,
            "client_secret": "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk",
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"]
        }) as response:
            response_json = await response.json()

            logging.info(f"Refreshed tokens {response_json['access_token']}")
            return response_json


async def get_tokens() -> dict:
    username = os.getenv("OSU_USERNAME")
    password = os.getenv("OSU_PASSWORD")

    async with ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data={
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": 5,
            "client_secret": "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk",
            "scope": "*"
        }) as response:
            response_json = await response.json()

            logging.info(f"Got tokens {response_json['access_token']}")
            return response_json