import os

import pytest

from kisters.water.rest_client import RESTClient
from kisters.water.rest_client.auth import OpenIDConnect

client_id = os.environ["HYDRAULIC_NETWORK_CLIENT_ID"]
client_secret = os.environ["HYDRAULIC_NETWORK_CLIENT_SECRET"]
service_url = os.environ["HYDRAULIC_NETWORK_STORE_URL"]
auth = OpenIDConnect(client_id, client_secret)


@pytest.fixture
def json_client():
    return RESTClient(url=service_url, authentication=auth)


@pytest.fixture
def msgpack_client():
    return RESTClient(url=service_url, authentication=auth, msgpack=True)


def test_get_str(json_client):
    networks = json_client.get("rest/networks")
    assert isinstance(networks, list)


def test_get_iter(json_client):
    networks = json_client.get(["rest", "networks"])
    assert isinstance(networks, list)


def test_get_msgpack(msgpack_client):
    networks = msgpack_client.get("rest/networks")
    assert isinstance(networks, list)
