import requests


def main():
    # Specify the URL you want to make a GET request to
    url = "http://127.0.0.1:8000/protected_data"

    # Define your custom headers (replace 'Your-API-Key' and 'your_api_key_value' with your actual header key and value)
    headers = {
        'api_key': 'ABC',  # Example authorization header
        'Content-Type': 'application/json',  # Example content type header
    }

    # Make a GET request with custom headers
    response = requests.get(url, headers=headers, timeout=2)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful, print response content
        print("Response content:")
        print(response.json())  # Assuming response content is JSON
    else:
        # Request failed, print error message
        print(f"Request failed with status code: {response.status_code}")


if __name__ == "__main__":
    main()
