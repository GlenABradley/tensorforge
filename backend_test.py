#!/usr/bin/env python3
"""
Tensor Forge Backend API Test Suite
Tests all API endpoints for the educational AI game
"""

import requests
import sys
import json
from datetime import datetime

class TensorForgeAPITester:
    def __init__(self, base_url="https://472b03e2-49c6-4e1d-a49b-f4a6b3bcb67a.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, message="", response_data=None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}: PASSED - {message}")
        else:
            print(f"❌ {name}: FAILED - {message}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "message": message,
            "response_data": response_data
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, expected_fields=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                self.log_test(name, False, f"Unsupported method: {method}")
                return False, {}

            print(f"   Status: {response.status_code}")
            
            # Check status code
            if response.status_code != expected_status:
                self.log_test(name, False, f"Expected status {expected_status}, got {response.status_code}")
                return False, {}

            # Parse JSON response
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                self.log_test(name, False, "Invalid JSON response")
                return False, {}

            # Check expected fields if provided
            if expected_fields:
                missing_fields = []
                for field in expected_fields:
                    if field not in response_json:
                        missing_fields.append(field)
                
                if missing_fields:
                    self.log_test(name, False, f"Missing fields: {missing_fields}")
                    return False, response_json

            self.log_test(name, True, "All checks passed", response_json)
            return True, response_json

        except requests.exceptions.RequestException as e:
            self.log_test(name, False, f"Request failed: {str(e)}")
            return False, {}
        except Exception as e:
            self.log_test(name, False, f"Unexpected error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200,
            expected_fields=["status", "message"]
        )

    def test_get_level_1(self):
        """Test getting level 1 data"""
        success, response = self.run_test(
            "Get Level 1",
            "GET", 
            "api/levels/1",
            200,
            expected_fields=["id", "title", "description", "available_components"]
        )
        
        if success:
            # Verify level 1 specific data
            if response.get("title") == "Train Your First AI Pet":
                print("   ✓ Level title correct")
            else:
                print(f"   ⚠ Unexpected title: {response.get('title')}")
            
            components = response.get("available_components", [])
            if len(components) >= 2:
                print(f"   ✓ Found {len(components)} components")
            else:
                print(f"   ⚠ Expected at least 2 components, found {len(components)}")
        
        return success, response

    def test_get_invalid_level(self):
        """Test getting invalid level"""
        return self.run_test(
            "Get Invalid Level",
            "GET",
            "api/levels/999",
            404
        )

    def test_train_shape_classifier_success(self):
        """Test successful shape classifier training"""
        # Create sample training data
        training_data = {
            "drawings": [
                {"points": [{"x": 10, "y": 10}, {"x": 20, "y": 20}, {"x": 30, "y": 10}]},
                {"points": [{"x": 5, "y": 5}, {"x": 15, "y": 5}, {"x": 15, "y": 15}, {"x": 5, "y": 15}]},
                {"points": [{"x": 25, "y": 25}, {"x": 35, "y": 35}, {"x": 45, "y": 25}]}
            ],
            "labels": ["triangle", "square", "triangle"]
        }
        
        success, response = self.run_test(
            "Train Shape Classifier - Success",
            "POST",
            "api/train-shape-classifier",
            200,
            data=training_data,
            expected_fields=["success", "score", "message"]
        )
        
        if success:
            if response.get("success"):
                print("   ✓ Training reported as successful")
            score = response.get("score", 0)
            print(f"   ✓ Training score: {score:.2%}")
            
            # Check for visual data
            if "visual_data" in response:
                visual_data = response["visual_data"]
                if "training_history" in visual_data:
                    print("   ✓ Training history included")
                if "predictions" in visual_data:
                    print("   ✓ Predictions included")
        
        return success, response

    def test_train_shape_classifier_insufficient_data(self):
        """Test training with insufficient data"""
        training_data = {
            "drawings": [
                {"points": [{"x": 10, "y": 10}, {"x": 20, "y": 20}]}
            ],
            "labels": ["circle"]
        }
        
        success, response = self.run_test(
            "Train Shape Classifier - Insufficient Data",
            "POST",
            "api/train-shape-classifier",
            200,
            data=training_data,
            expected_fields=["success", "score", "message"]
        )
        
        if success:
            if not response.get("success"):
                print("   ✓ Correctly rejected insufficient data")
            else:
                print("   ⚠ Should have rejected insufficient data")
        
        return success, response

    def test_simulate_build(self):
        """Test component build simulation"""
        build_data = {
            "components": [
                {"name": "Neural Layer", "args": []},
                {"name": "Activation Function", "args": []}
            ],
            "level_id": 1
        }
        
        success, response = self.run_test(
            "Simulate Build",
            "POST",
            "api/simulate-build",
            200,
            data=build_data,
            expected_fields=["success", "score", "message"]
        )
        
        if success:
            if response.get("success"):
                print("   ✓ Build simulation successful")
            if "visual_data" in response:
                print("   ✓ Visual data included")
        
        return success, response

    def test_simulate_build_invalid_level(self):
        """Test build simulation with invalid level"""
        build_data = {
            "components": [{"name": "Neural Layer", "args": []}],
            "level_id": 999
        }
        
        return self.run_test(
            "Simulate Build - Invalid Level",
            "POST",
            "api/simulate-build",
            404,
            data=build_data
        )

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Tensor Forge API Tests")
        print("=" * 50)
        
        # Test all endpoints
        self.test_health_check()
        self.test_get_level_1()
        self.test_get_invalid_level()
        self.test_train_shape_classifier_success()
        self.test_train_shape_classifier_insufficient_data()
        self.test_simulate_build()
        self.test_simulate_build_invalid_level()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 All tests passed! Backend API is working correctly.")
            return 0
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} test(s) failed. Check the issues above.")
            return 1

def main():
    """Main test runner"""
    # Check if custom URL provided
    base_url = "https://472b03e2-49c6-4e1d-a49b-f4a6b3bcb67a.preview.emergentagent.com"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing Tensor Forge API at: {base_url}")
    
    tester = TensorForgeAPITester(base_url)
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())