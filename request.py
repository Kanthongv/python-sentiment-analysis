import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"

def main():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("Request successful")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def passcode(code: str) -> str:
    return "Nothing to see here"


if __name__ == "__main__":
    main()
