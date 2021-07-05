from aiohttp import ClientSession

async def get_users(tokens: dict, user_ids: list) -> dict:
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }

    query_params = []
    for user_id in user_ids:
        query_params.append((
            "ids[]", user_id
        ))

    async with ClientSession() as session:
        async with session.get("https://osu.ppy.sh/api/v2/users", params=query_params, headers=headers) as response:
            return await response.json()