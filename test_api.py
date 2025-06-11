import requests
import json


def pretty_print_json(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))


def get_device(serial):
    url = f"http://localhost:5000/api/device/{serial}"
    response = requests.get(url)

    if response.status_code == 200:
        data_dict = response.json()
        pretty_print_json(data_dict)
        return data_dict
    else:
        print(f"GET failed with status code {response.status_code}: {response.text}")
        return None


def post_device(serial):
    url = "http://localhost:5000/api/device"
    data = {"serial": serial}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code in (200, 201):
        pretty_print_json(response.json())
        return response.json()
    else:
        print(f"POST failed with status code {response.status_code}: {response.text}")
        return None


# Example usage:
serial_number = "SN003"

print("GET device:")
get_device(serial_number)

print("\nPOST device:")
post_device(serial_number)