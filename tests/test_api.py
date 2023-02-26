import requests
from pytest_voluptuous import S

from schemas.user import create_single_user, login_successful, register_single_user, unregister_single_user, \
    login_unsuccessful

base_url = "https://reqres.in/"


def test_register_successful():
    register_user = requests.post(f"{base_url}api/register", {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    })

    assert register_user.status_code == 200
    assert S(register_single_user) == register_user.json()
    assert register_user.json()['id']
    assert register_user.json()['token']


def test_register_unsuccessful():
    register_user = requests.post(f"{base_url}api/register", {
        "email": "sydney@fife"
    })

    assert register_user.status_code == 400
    assert S(unregister_single_user) == register_user.json()
    #assert register_user.json()['error'] == ['Missing password']


def test_login_successful():
    login_user = requests.post(f"{base_url}api/login", {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })
    assert login_user.status_code == 200
    assert S(login_successful) == login_user.json()
    assert login_user.json()['token']


def test_login_unsuccessful():
    unlogin_user = requests.post(f"{base_url}api/login", {
        "email": "peter@klaven"
    })
    assert unlogin_user.status_code == 400
    assert S(login_unsuccessful) == unlogin_user.json()
    #assert unlogin_user.json()['error'] == ['Missing password']


def test_create():
    create_user = requests.post(f"{base_url}api/users", {
        "name": "morpheus",
        "job": "leader",
        "id": "778",
        "createdAt": "2023-02-26T14:29:35.691Z"
    })
    assert create_user.status_code == 201
    assert S(create_single_user) == create_user.json()


def test_delete():
    delete_user = requests.delete(f"{base_url}api/users/2")

    assert delete_user.status_code == 204
