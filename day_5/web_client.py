import requests
import time

URL = "http://192.168.100.220:8080/get_restaurant_menu"

def fetch_menu():
    while True:
        try:
            response = requests.get(URL, timeout=5)
            response.raise_for_status()  
            print("Status:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

if __name__ == "__main__":
    fetch_menu()