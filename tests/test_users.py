import os
import pytest
from testcontainers.postgres import PostgresContainer
from app.model.users import create_table, delete_all_users, get_all_users, User
from app.service.user_service import create_user, get_cached_user_by_email, delete_user_from_cache_and_database
from testcontainers.redis import RedisContainer


postgres = PostgresContainer("postgres:16-alpine")
redis_container = RedisContainer("redis:5.0.3-alpine")


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()
    redis_container.start()

    def remove_container():
        postgres.stop()
        redis_container.stop()

    request.addfinalizer(remove_container)

    os.environ["DB_CONN"] = postgres.get_connection_url()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = postgres.get_exposed_port(5432)
    os.environ["DB_USERNAME"] = postgres.POSTGRES_USER
    os.environ["DB_PASSWORD"] = postgres.POSTGRES_PASSWORD
    os.environ["DB_NAME"] = postgres.POSTGRES_DB
    os.environ["REDIS_HOST"] = redis_container.get_container_host_ip()
    os.environ["REDIS_PORT"] = redis_container.get_exposed_port(6379)
    create_table()


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    delete_all_users()


def test_get_all_users():
    create_user("sameer", "sameer.shukla@gmail.com", True)
    user_list = get_all_users()
    assert len(user_list) == 1


def test_get_user_by_email():
    create_user("sameer", "sameer.shukla@gmail.com", True)
    user_dict = get_cached_user_by_email("sameer.shukla@gmail.com")
    user = User(**user_dict)
    assert user.username == "sameer"
    assert user.email == "sameer.shukla@gmail.com"


def test_delete_user():
    create_user("sameer", "sameer.shukla@gmail.com", True)
    user_dict = get_cached_user_by_email("sameer.shukla@gmail.com")
    print(user_dict)
    user = User(**user_dict)
    print('user:', user)
    assert user.username == "sameer"
    assert user.email == "sameer.shukla@gmail.com"
    delete_user_from_cache_and_database("sameer.shukla@gmail.com")
    user = get_cached_user_by_email("sameer.shukla@gmail.com")
    assert user is None

