import requests
from utils.load_schema import load_schema
import jsonschema
from tests.conftest import default_url


def test_get_list_of_resources_status_code(default_url):
    result = requests.get(f'{default_url}unknown')

    assert result.status_code == 200


def test_delete_user_success(default_url):
    user_id = 3
    result = requests.delete(f'{default_url}users/{user_id}')

    assert result.status_code == 204
    assert result.text == ''


def test_update_user_success(default_url):
    user_id = 2
    result = requests.put(f'{default_url}users/{user_id}',
                          data={"name": "John", "job": "driver"})

    assert result.status_code == 200
    assert result.json()['job'] == 'driver'


def test_update_user_without_data_status_code(default_url):
    result = requests.put(f'{default_url}users')

    assert result.status_code == 404


def test_wrong_endpoint_login(default_url):
    result = requests.put(f'{default_url}loginn',
                          data={"email": "eve.holt@reqres.in", "password": "cityslicka"})

    assert result.status_code == 404

def test_create_user(default_url):
    result = requests.post(f'{default_url}users',
                          data={"name": "John", "job": "driver"})

    assert result.status_code == 201


# SCHEMAS ASSERTS

def test_schema_get_list_resources(default_url):
    result = requests.get(f'{default_url}unknown')
    schema = load_schema('get_list_resource.json')

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_schema_successful_login(default_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    result = requests.post(f'{default_url}login', data=payload)
    schema = load_schema('post_login_successful.json')

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_schema_unsuccessful_login(default_url):
    payload = {
        "email": "eve.holt@reqres.in"
    }
    result = requests.post(f'{default_url}login', data=payload)
    schema = load_schema('post_login_unsuccessful.json')

    assert result.status_code == 400
    jsonschema.validate(result.json(), schema)


def test_schema_give_token_after_register(default_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    result = requests.post(f'{default_url}register', data=payload)
    schema = load_schema('post_register_successful.json')

    jsonschema.validate(result.json(), schema)
    assert result.json()["token"] != ""
