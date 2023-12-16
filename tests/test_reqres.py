import requests
from utils import load_schema
import jsonschema


def test_get_list_of_resources_status_code():
    url = 'https://reqres.in/api/unknown'
    result = requests.get(url)

    assert result.status_code == 200


def test_delete_user_success():
    user_id = 3
    url = f'https://reqres.in/api/users/{user_id}'
    result = requests.delete(url)

    assert result.status_code == 204
    assert result.text == ''


def test_update_user_success():
    result = requests.put('https://reqres.in/api/users/2', data={"name": "John", "job": "driver"})

    assert result.status_code == 200
    assert result.json()['job'] == 'driver'


def test_update_user_without_data_status_code():
    result = requests.put('https://reqres.in/api/users')

    assert result.status_code == 404


def test_wrong_endpoint_login():
    result = requests.put('https://reqres.in/api/loginn',
                          data={"email": "eve.holt@reqres.in", "password": "cityslicka"})

    assert result.status_code == 404


# SCHEMAS ASSERTS

def test_schema_get_list_resources():
    url = 'https://reqres.in/api/unknown'
    result = requests.get(url)
    schema = load_schema('get_list_resource.json')

    jsonschema.validate(result.json(), schema)


def test_schema_successful_login():
    url = 'https://reqres.in/api/login'
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    result = requests.post(url, data=payload)
    schema = load_schema('post_login_successful.json')

    jsonschema.validate(result.json(), schema)


def test_schema_unsuccessful_login():
    url = 'https://reqres.in/api/login'
    payload = {
        "email": "eve.holt@reqres.in"
    }
    result = requests.post(url, data=payload)
    schema = load_schema('post_login_unsuccessful.json')

    assert result.status_code == 400
    jsonschema.validate(result.json(), schema)


def test_schema_give_token_after_register():
    url = 'https://reqres.in/api/register'
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    result = requests.post(url, data=payload)
    schema = load_schema('post_register_successful.json')

    jsonschema.validate(result.json(), schema)
    assert result.json()["token"] != ""
