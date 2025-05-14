"""Test the complete authentication flow."""

import requests
import json
import time
from typing import Optional, Dict


class AuthFlow:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        
    def _print_request(self, method: str, url: str, headers: Dict, data: Optional[Dict] = None):
        print(f"\n{method} Request:")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        if data:
            print(f"Data: {json.dumps(data, indent=2)}")
            
    def _print_response(self, response: requests.Response):
        print(f"\nStatus Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
            
    def health_check(self) -> bool:
        """Test the health check endpoint."""
        url = f"{self.base_url}/api/v1/health"
        
        try:
            self._print_request("GET", url, {})
            response = requests.get(url)
            self._print_response(response)
            return response.status_code == 200 and response.json()["status"] == "ok"
        except Exception as e:
            print(f"\nError: {str(e)}")
            return False
            
    def register(self, email: str, password: str, full_name: str, language: str = "pt-BR") -> bool:
        """Test user registration."""
        url = f"{self.base_url}/api/v1/auth/register"
        headers = {"Content-Type": "application/json"}
        data = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "language": language
        }
        
        try:
            self._print_request("POST", url, headers, data)
            response = requests.post(url, headers=headers, json=data)
            self._print_response(response)
            
            if response.status_code == 201:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                return True
            return False
        except Exception as e:
            print(f"\nError: {str(e)}")
            return False
            
    def login(self, email: str, password: str) -> bool:
        """Test user login."""
        url = f"{self.base_url}/api/v1/auth/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": email,
            "password": password
        }
        
        try:
            self._print_request("POST", url, headers, data)
            response = requests.post(url, headers=headers, data=data)
            self._print_response(response)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                return True
            return False
        except Exception as e:
            print(f"\nError: {str(e)}")
            return False


def test_auth_flow():
    """Run the complete authentication flow test."""
    flow = AuthFlow()
    
    print("\n=== Testing Health Check ===")
    if not flow.health_check():
        print("❌ Health check failed")
        return False
    print("✅ Health check passed")
    
    # Generate a unique email using timestamp
    timestamp = int(time.time())
    email = f"test{timestamp}@example.com"
    password = "Test123!"
    full_name = "Test User"
    
    print("\n=== Testing Registration ===")
    if not flow.register(email, password, full_name):
        print("❌ Registration failed")
        return False
    print("✅ Registration passed")
    
    print("\n=== Testing Login ===")
    if not flow.login(email, password):
        print("❌ Login failed")
        return False
    print("✅ Login passed")
    
    print("\n🎉 All tests passed successfully!")
    return True


if __name__ == "__main__":
    test_auth_flow()
