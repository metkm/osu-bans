from api import get_users
from utils import difference_between_lists, iterate_list
from tokens import get_tokens, refresh_tokens
import asyncio
import database


db_helper = database.Database()
tokens = {}


async def refresh_tokens_task(tokens: dict):
    while True:
        await asyncio.sleep(86000)
        tokens = refresh_tokens(tokens)


def write_banned(user_id: int):
    user = db_helper.set_user_banned(user_id)

    if not user:
        return

    with open("banned.txt", "a", encoding="utf-8") as file:
        file.write(f"Banned! {user['user']['id']} {user['user']['username']} \n")


async def main():
    tokens = await get_tokens()

    asyncio.create_task(refresh_tokens_task(tokens))
    while True: # main loop of the program
        user_ids = db_helper.get_user_ids()
        for user_ids in iterate_list(user_ids, 250):
            coros = [get_users(tokens, fifty_user_id) for fifty_user_id in iterate_list(user_ids, 50)] # 5 requests at the same time
            responses = await asyncio.gather(*coros)
            
            response_user_ids = []
            for response in responses:
                for user in response["users"]:
                    response_user_ids.append(
                        user["id"]
                    )
            
            different_ids = difference_between_lists(user_ids, response_user_ids)
            for diff_id in different_ids:
                write_banned(diff_id)

            print("sleeping 60 seconds!")
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
