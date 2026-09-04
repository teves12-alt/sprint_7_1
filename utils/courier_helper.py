import random
import string
import requests

from config import BASE_URL


def generate_random_login():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))


def generate_random_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def generate_random_first_name():
    return "".join(random.choices(string.ascii_letters, k=6))


def register_new_courier_and_return_login_password():
    login = generate_random_login()
    password = generate_random_password()
    first_name = generate_random_first_name()

    payload = {"login": login, "password": password, "firstName": first_name}
    resp = requests.post(f"{BASE_URL}/courier", json=payload)
    if resp.status_code == 201 and resp.json().get("ok") is True:
        return [login, password, first_name]
    return []
