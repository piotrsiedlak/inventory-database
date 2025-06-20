import requests
import json

BASE_URL = "http://localhost:5000"

def pretty_print_json(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

def get_device(serial):
    url = f"{BASE_URL}/api/device/{serial}"
    response = requests.get(url)
    return response

def post_device(serial):
    url = f"{BASE_URL}/api/device"
    data = {"serial": serial}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    return response

def test_post_device():
    serial_number = "SN003"
    response = post_device(serial_number)

    assert response.status_code in (200, 201), f"POST failed: {response.status_code} {response.text}"
    data = response.json()
    pretty_print_json(data)

    assert serial_number in data
    assert isinstance(data[serial_number], dict)

def test_get_device():
    serial_number = "SN003"
    response = get_device(serial_number)

    assert response.status_code == 200, f"GET failed: {response.status_code} {response.text}"
    data = response.json()
    pretty_print_json(data)

    assert serial_number in data
    assert "pdu" in data[serial_number]
    assert "port" in data[serial_number]
