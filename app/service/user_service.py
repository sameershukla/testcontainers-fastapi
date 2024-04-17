from app.model.users import create_user_db, get_user_by_email, delete_user_by_email, get_all_users
from app.service.cache_service import UserCache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_user(username, email, is_active):
    user = create_user_db(username, email, is_active)
    logger.info(f"User created: {user.username}, {user.email}")
    if user is not None:
        user_cache = UserCache()
        user_cache.push_data(user.email, user.__dict__)
        logger.info(f"User stored in cache with key: {user.email}")
    return user


def get_cached_user_by_email(email):
    user_cache = UserCache()
    user = user_cache.retrieve_data(email)
    logger.info(f"User found in cache: {user}")
    if user is None:
        logger.debug(f"User not found in cache, querying db")
        return get_user_by_email(email)
    else:
        return user


def delete_user_from_cache_and_database(email):
    user_cache = UserCache()
    if user_cache is not None:
        delete_user_by_email(email)
        user_cache.delete_data(email)
        logger.info(f"User deleted from cache and database")
    else:
        return None


class UserService:

    def __init__(self):
        pass  # Empty method
