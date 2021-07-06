import os
import pymongo
from datetime import datetime


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

    def update_date_checkeds(self, user_ids: list):
        utc_now = datetime.utcnow()
        timestamp = utc_now.timestamp()

        self.track.update_many({
            "user.id": {
                "$in": user_ids
            }
        }, {
            "$set": {
                "date_checked": timestamp
            }
        })


if __name__ == "__main__":
    db_helper = Database()
    db_helper.update_date_checked([
        3674590, 2070822, 10164681
    ])
