from aiohttp import ClientSession
import os


async def refresh_tokens(tokens: dict) -> dict:
    async with ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data={
            "client_id": 5,
            "client_secret": "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk",
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"]
        }) as response:
            return await response.json()


async def get_tokens() -> dict:
    username = os.getenv("osu_username")
    password = os.getenv("osu_password")

    async with ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data={
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": 5,
            "client_secret": "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk",
            "scope": "*"
        }) as response:
            return await response.json()