import requests

def test_health():
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    test_health()
