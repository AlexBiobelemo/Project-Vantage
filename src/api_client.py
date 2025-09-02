import requests
from models import VPNNode

# URL with localhost IP address

API_URL = "http://127.0.0.1:5001/api/v1/nodes"


def fetch_nodes() -> list[VPNNode]:
    """
    Fetches the list of VPN nodes from the mock API.
    Returns a list of VPNNode objects.
    """
    try:
        response = requests.get(API_URL, timeout=3)
        # Raise an exception for bad status codes (4xx or 5xx)

        response.raise_for_status()

        data = response.json()

        # Convert the raw dictionary data into VPNNode objects

        nodes = [VPNNode(**node_data) for node_data in data]
        return nodes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nodes from API: {e}")
        # Return an empty list if the API can't be reached

        return []
