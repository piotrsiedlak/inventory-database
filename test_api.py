# test_api.py

import requests
import json

BASE_URL = "http://localhost:5000/api/device"
TEST_SERIAL = "TEST_SN001"

def delete_device(serial):
    """Pomocnicza funkcja do usuwania urządzenia (ignoruje błąd 404)."""
    url = f"{BASE_URL}/{serial}"
    requests.delete(url)

def test_post_device():
    delete_device(TEST_SERIAL)  # przed testem

    response = requests.post(BASE_URL, json={"serial": TEST_SERIAL})
    assert response.status_code in (200, 201)
    data = response.json()
    assert TEST_SERIAL in data

    delete_device(TEST_SERIAL)  # po teście

def test_get_device():
    delete_device(TEST_SERIAL)
    requests.post(BASE_URL, json={"serial": TEST_SERIAL})

    response = requests.get(f"{BASE_URL}/{TEST_SERIAL}")
    assert response.status_code == 200
    data = response.json()
    assert TEST_SERIAL in data

    delete_device(TEST_SERIAL)
