"""
Manual Test Client for FastAPI Finance Dashboard Server

This script provides a comprehensive testing interface for all API endpoints
with formatted example messages and responses.

Usage:
    python test_client.py

Features:
    - Interactive menu system
    - All 11 endpoints with example data
    - Formatted request/response display
    - Error handling and logging
    - Session management for testing
"""

import requests
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
CHAT_HISTORY_DIR = Path("chat_history")

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_section(text: str):
    """Print a formatted section title"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}► {text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'-'*70}{Colors.ENDC}")


def print_request(method: str, endpoint: str, data: Optional[Dict] = None):
    """Print formatted request information"""
    print(f"{Colors.CYAN}{Colors.BOLD}REQUEST:{Colors.ENDC}")
    print(f"  Method: {Colors.YELLOW}{method}{Colors.ENDC}")
    print(f"  URL: {Colors.YELLOW}{API_BASE_URL}{endpoint}{Colors.ENDC}")
    if data:
        print(f"  Data: {Colors.YELLOW}{json.dumps(data, indent=4)}{Colors.ENDC}")


def print_response(response: requests.Response):
    """Print formatted response information"""
    status_color = Colors.GREEN if response.status_code < 400 else Colors.RED
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}RESPONSE:{Colors.ENDC}")
    print(f"  Status: {status_color}{response.status_code}{Colors.ENDC}")
    
    try:
        data = response.json()
        print(f"  Body:\n{Colors.GREEN}{json.dumps(data, indent=4)}{Colors.ENDC}")
    except:
        print(f"  Body:\n{Colors.GREEN}{response.text}{Colors.ENDC}")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.ENDC}")


class TestClient:
    """Test client for API endpoints"""
    
    def __init__(self):
        self.session = requests.Session()
        self.test_username = "testuser"
        self.test_session_id = None
        self.created_sessions = []
    
    def check_server(self) -> bool:
        """Check if server is running"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health")
            return response.status_code == 200
        except:
            return False
    
    # =====================================================================
    # TRADING ENDPOINTS
    # =====================================================================
    
    def test_etf_options(self):
        """GET /api/trading/etf-options"""
        print_section("TEST: Get ETF Options")
        print_request("GET", "/api/trading/etf-options")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/api/trading/etf-options")
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Retrieved {data.get('count', 0)} ETF options")
            else:
                print_error(f"Failed to get ETF options: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_stock_options(self):
        """GET /api/trading/stock-options"""
        print_section("TEST: Get Stock Options")
        print_request("GET", "/api/trading/stock-options")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/api/trading/stock-options")
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Retrieved {data.get('count', 0)} stock options")
            else:
                print_error(f"Failed to get stock options: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_max_date(self):
        """GET /api/trading/max-date/{table_name}"""
        print_section("TEST: Get Max Date from Table")
        
        table_name = "histdailyprice7"
        endpoint = f"/api/trading/max-date/{table_name}"
        print_request("GET", endpoint)
        
        try:
            response = self.session.get(f"{API_BASE_URL}{endpoint}")
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Max date for {table_name}: {data.get('max_date')}")
            else:
                print_error(f"Failed to get max date: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_custom_query(self):
        """POST /api/trading/custom-query"""
        print_section("TEST: Execute Custom Query")
        
        # Simple test query
        query = "SELECT 1 as test"
        endpoint = f"/api/trading/custom-query?query={query}"
        print_request("POST", endpoint)
        
        try:
            response = self.session.post(f"{API_BASE_URL}{endpoint}")
            print_response(response)
            
            if response.status_code == 200:
                print_success("Custom query executed successfully")
            else:
                print_error(f"Failed to execute query: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    # =====================================================================
    # CHAT ENDPOINTS
    # =====================================================================
    
    def test_create_session(self):
        """POST /api/chat/session"""
        print_section("TEST: Create Chat Session")
        
        endpoint = f"/api/chat/session?username={self.test_username}"
        print_request("POST", endpoint)
        
        try:
            response = self.session.post(f"{API_BASE_URL}{endpoint}")
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                self.test_session_id = data.get('id')
                self.created_sessions.append(self.test_session_id)
                print_success(f"Chat session created: {self.test_session_id}")
                return self.test_session_id
            else:
                print_error(f"Failed to create session: {response.status_code}")
                return None
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return None
    
    def test_get_sessions(self):
        """GET /api/chat/sessions/{username}"""
        print_section("TEST: Get User Sessions")
        
        endpoint = f"/api/chat/sessions/{self.test_username}"
        print_request("GET", endpoint)
        
        try:
            response = self.session.get(f"{API_BASE_URL}{endpoint}")
            print_response(response)
            
            if response.status_code == 200:
                sessions = response.json()
                print_success(f"Retrieved {len(sessions)} session(s)")
                for session in sessions:
                    print(f"  - {Colors.YELLOW}{session.get('id')}{Colors.ENDC} "
                          f"({session.get('message_count', 0)} messages)")
            else:
                print_error(f"Failed to get sessions: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_save_message(self):
        """POST /api/chat/message"""
        print_section("TEST: Save Chat Message")
        
        if not self.test_session_id:
            print_error("No session ID. Create a session first.")
            return
        
        message_data = {
            "username": self.test_username,
            "session_id": self.test_session_id,
            "content": "Hello! This is a test message.",
            "message_type": "text"
        }
        
        endpoint = "/api/chat/message"
        print_request("POST", endpoint, message_data)
        
        try:
            response = self.session.post(
                f"{API_BASE_URL}{endpoint}",
                data=message_data
            )
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Message saved: {data.get('message_id')}")
            else:
                print_error(f"Failed to save message: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_get_history(self):
        """GET /api/chat/history/{username}/{session_id}"""
        print_section("TEST: Get Chat History")
        
        if not self.test_session_id:
            print_error("No session ID. Create a session first.")
            return
        
        endpoint = f"/api/chat/history/{self.test_username}/{self.test_session_id}"
        print_request("GET", endpoint)
        
        try:
            response = self.session.get(f"{API_BASE_URL}{endpoint}")
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get('messages', [])
                print_success(f"Retrieved {len(messages)} message(s)")
            else:
                print_error(f"Failed to get history: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_upload_image(self):
        """POST /api/chat/upload/{username}/{session_id}"""
        print_section("TEST: Upload Chat Image")
        
        if not self.test_session_id:
            print_error("No session ID. Create a session first.")
            return
        
        # Create a simple test image
        test_image_path = Path("test_image.jpg")
        if not test_image_path.exists():
            print_info("Creating a test image file...")
            # Create a minimal JPEG
            with open(test_image_path, 'wb') as f:
                f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
                       b'\xff\xd9')
        
        endpoint = f"/api/chat/upload/{self.test_username}/{self.test_session_id}"
        print_request("POST", endpoint)
        print_info("Uploading image file: test_image.jpg")
        
        try:
            with open(test_image_path, 'rb') as f:
                files = {'file': ('test_image.jpg', f, 'image/jpeg')}
                response = self.session.post(
                    f"{API_BASE_URL}{endpoint}",
                    files=files
                )
            
            print_response(response)
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Image uploaded: {data.get('message_id')}")
            else:
                print_error(f"Failed to upload image: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_delete_session(self):
        """DELETE /api/chat/session/{username}/{session_id}"""
        print_section("TEST: Delete Chat Session")
        
        if not self.test_session_id:
            print_error("No session ID to delete.")
            return
        
        endpoint = f"/api/chat/session/{self.test_username}/{self.test_session_id}"
        print_request("DELETE", endpoint)
        
        try:
            response = self.session.delete(f"{API_BASE_URL}{endpoint}")
            print_response(response)
            
            if response.status_code == 200:
                print_success(f"Session deleted: {self.test_session_id}")
                self.test_session_id = None
            else:
                print_error(f"Failed to delete session: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    def test_download_file(self):
        """GET /api/chat/file/{username}/{session_id}/{filename}"""
        print_section("TEST: Download Chat File")
        
        if not self.test_session_id:
            print_error("No session ID. Create a session first.")
            return
        
        # Try to download the test image
        filename = "image_test.jpg"
        endpoint = f"/api/chat/file/{self.test_username}/{self.test_session_id}/{filename}"
        print_request("GET", endpoint)
        
        try:
            response = self.session.get(f"{API_BASE_URL}{endpoint}")
            
            if response.status_code == 200:
                print_success(f"File downloaded: {filename}")
                print(f"  Size: {len(response.content)} bytes")
            elif response.status_code == 404:
                print_info("File not found (this is expected if image wasn't uploaded)")
            else:
                print_error(f"Failed to download file: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")


def print_menu():
    """Print the main menu"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}FASTAPI TEST CLIENT - MAIN MENU{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*70}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}TRADING ENDPOINTS:{Colors.ENDC}")
    print("  1. GET /api/trading/etf-options")
    print("  2. GET /api/trading/stock-options")
    print("  3. GET /api/trading/max-date/{table}")
    print("  4. POST /api/trading/custom-query")
    
    print(f"\n{Colors.BOLD}CHAT ENDPOINTS:{Colors.ENDC}")
    print("  5. POST /api/chat/session (Create)")
    print("  6. GET /api/chat/sessions/{username} (List)")
    print("  7. POST /api/chat/message (Save)")
    print("  8. POST /api/chat/upload/{user}/{session} (Upload)")
    print("  9. GET /api/chat/history/{user}/{session} (Get History)")
    print("  10. DELETE /api/chat/session/{user}/{session} (Delete)")
    print("  11. GET /api/chat/file/{user}/{session}/{file} (Download)")
    
    print(f"\n{Colors.BOLD}UTILITIES:{Colors.ENDC}")
    print("  12. Run All Tests")
    print("  13. Show Current Session Info")
    print("  0. Exit")
    
    print(f"\n{Colors.CYAN}{'-'*70}{Colors.ENDC}")


def run_all_tests(client: TestClient):
    """Run all tests sequentially"""
    print_header("RUNNING ALL TESTS")
    
    tests = [
        ("ETF Options", client.test_etf_options),
        ("Stock Options", client.test_stock_options),
        ("Max Date", client.test_max_date),
        ("Custom Query", client.test_custom_query),
        ("Create Session", client.test_create_session),
        ("Save Message", client.test_save_message),
        ("Get History", client.test_get_history),
        ("Get Sessions", client.test_get_sessions),
        ("Upload Image", client.test_upload_image),
        ("Download File", client.test_download_file),
        ("Delete Session", client.test_delete_session),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print_error(f"Test failed: {str(e)}")
            failed += 1
        
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"{Colors.GREEN}✓ Passed: {passed}{Colors.ENDC}")
    print(f"{Colors.RED}✗ Failed: {failed}{Colors.ENDC}")
    print(f"{Colors.BLUE}Total: {passed + failed}{Colors.ENDC}\n")


def show_session_info(client: TestClient):
    """Show current session information"""
    print_section("Current Session Information")
    print(f"  Test Username: {Colors.YELLOW}{client.test_username}{Colors.ENDC}")
    print(f"  Current Session ID: {Colors.YELLOW}{client.test_session_id or 'None'}{Colors.ENDC}")
    print(f"  Created Sessions: {Colors.YELLOW}{len(client.created_sessions)}{Colors.ENDC}")
    
    if client.created_sessions:
        print(f"\n  Session IDs:")
        for session_id in client.created_sessions:
            print(f"    - {Colors.CYAN}{session_id}{Colors.ENDC}")


def main():
    """Main function"""
    print_header("FASTAPI FINANCE DASHBOARD - TEST CLIENT")
    
    # Initialize client
    client = TestClient()
    
    # Check server
    print("Checking server connection...")
    if not client.check_server():
        print_error("Cannot connect to server at http://localhost:8000")
        print_info("Make sure the server is running: python main.py")
        sys.exit(1)
    
    print_success("Connected to server!")
    
    # Main loop
    while True:
        print_menu()
        
        try:
            choice = input(f"{Colors.BOLD}Enter your choice (0-13): {Colors.ENDC}").strip()
            
            if choice == "0":
                print_info("Exiting test client...")
                break
            
            elif choice == "1":
                client.test_etf_options()
            elif choice == "2":
                client.test_stock_options()
            elif choice == "3":
                client.test_max_date()
            elif choice == "4":
                client.test_custom_query()
            elif choice == "5":
                client.test_create_session()
            elif choice == "6":
                client.test_get_sessions()
            elif choice == "7":
                client.test_save_message()
            elif choice == "8":
                client.test_upload_image()
            elif choice == "9":
                client.test_get_history()
            elif choice == "10":
                client.test_delete_session()
            elif choice == "11":
                client.test_download_file()
            elif choice == "12":
                run_all_tests(client)
            elif choice == "13":
                show_session_info(client)
            else:
                print_error("Invalid choice. Please try again.")
            
            # Wait for user to read output
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
        
        except KeyboardInterrupt:
            print_info("\nExiting test client...")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
