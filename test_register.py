import requests
import json

def test_register():
    url = "http://localhost:8000/api/v1/auth/register"
    headers = {"Content-Type": "application/json"}
    data = {
        "email": "test3@example.com",
        "password": "Test123!",
        "language": "pt-BR",
        "full_name": "Test User"
    }
    
    try:
        print("\nRequest:")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, indent=2)}")

        response = requests.post(url, headers=headers, json=data)
        print(f"\nStatus Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    test_register()
