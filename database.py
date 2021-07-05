import os
import pymongo


class Database():
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv("MONGO_URL"))
        self.db = self.client["users"]
        self.track = self.db["track"]
        self.banned = self.db["banned"]

    def add_users(self, users: dict):
        self.track.insert_many(users)

    def add_user(self, user: dict):
        self.track.insert_one(user)

    def delete_user(self, user_id: int):
        self.track.delete_one({
            "user.id": user_id
        })

    def delete_users(self, user_ids: list):
        self.track.delete_many({
            "user.id": {
                "$in": user_ids
            }
        })

    def get_user(self, user_id: int):
        self.track.find_one({
            "user.id": user_id
        })

    def get_user_ids(self):
        users = self.track.find()
        return [user["user"]["id"] for user in users]

    def set_user_banned(self, user_id: int):
        user = self.track.find_one({
            "user.id": user_id
        })

        if not user:
            print(f"{user_id} doesnt exists in database")
            return
            
        self.track.delete_one({
            "user.id": user_id
        })
        self.banned.insert_one(user)

        return user
