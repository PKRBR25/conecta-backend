import requests
import json

def test_login():
    url = "http://localhost:8000/api/v1/auth/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "username": "test3@example.com",
        "password": "Test123!"
    }
    
    try:
        print("\nRequest:")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")

        response = requests.post(url, headers=headers, data=data)
        print(f"\nStatus Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    test_login()
