import redis
import json
import os
from app.model.users import User


class UserCache:
    def __init__(self):
        host = os.getenv("REDIS_HOST", "127.0.0.1")
        port = os.getenv("REDIS_PORT", "6379")
        db = os.getenv("REDIS_DB", 0)
        print('Host:', host)
        print('port:', port)
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def push_data(self, key, data):
        """Pushes data to Redis cache."""
        if isinstance(data, dict):
            data = json.dumps(self.objToDict(data))
        return self.redis_client.set(key, data)

    def retrieve_data(self, key):
        """Retrieves data from Redis cache."""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        else:
            return None

    def delete_data(self, key):
        """Deletes data from Redis cache."""
        return self.redis_client.delete(key)

    def objToDict(user: User):
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
        return user_dict
