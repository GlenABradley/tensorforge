#!/usr/bin/env python3
"""
Enhanced Tensor Forge Backend API Test Suite
Tests all enhanced API endpoints including hints, components, and progress tracking
"""

import requests
import sys
import json
from datetime import datetime

class EnhancedTensorForgeAPITester:
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

    def test_get_components(self):
        """Test getting all available components"""
        success, response = self.run_test(
            "Get Components",
            "GET",
            "api/components",
            200,
            expected_fields=["components"]
        )
        
        if success:
            components = response.get("components", [])
            print(f"   ✓ Found {len(components)} components")
            
            # Check for expected components
            expected_components = ["neural_layer", "activation_relu", "dense_layer", "dropout", "tensor_add", "tensor_multiply"]
            found_components = [comp.get("id", "") for comp in components]
            
            for expected in expected_components:
                if expected in found_components:
                    print(f"   ✓ Found component: {expected}")
                else:
                    print(f"   ⚠ Missing component: {expected}")
        
        return success, response

    def test_get_level_2(self):
        """Test getting level 2 data"""
        success, response = self.run_test(
            "Get Level 2",
            "GET", 
            "api/levels/2",
            200,
            expected_fields=["id", "title", "description", "available_components"]
        )
        
        if success:
            if response.get("id") == 2:
                print("   ✓ Level ID correct")
            components = response.get("available_components", [])
            if len(components) >= 3:
                print(f"   ✓ Found {len(components)} components for Level 2")
            else:
                print(f"   ⚠ Expected at least 3 components, found {len(components)}")
        
        return success, response

    def test_get_level_4(self):
        """Test getting level 4 data (mini-boss level)"""
        success, response = self.run_test(
            "Get Level 4",
            "GET", 
            "api/levels/4",
            200,
            expected_fields=["id", "title", "description", "available_components"]
        )
        
        if success:
            if response.get("id") == 4:
                print("   ✓ Level 4 ID correct")
            components = response.get("available_components", [])
            print(f"   ✓ Found {len(components)} components for Level 4")
        
        return success, response

    def test_hint_system(self):
        """Test adaptive hint system"""
        hint_data = {
            "level_id": 1,
            "player_state": {
                "components": ["neural_layer"],
                "training_data_count": 0,
                "last_error": "insufficient_data"
            }
        }
        
        success, response = self.run_test(
            "Get Adaptive Hint",
            "POST",
            "api/hint",
            200,
            data=hint_data,
            expected_fields=["hint", "type"]
        )
        
        if success:
            hint_text = response.get("hint", "")
            hint_type = response.get("type", "")
            print(f"   ✓ Hint type: {hint_type}")
            print(f"   ✓ Hint text: {hint_text[:50]}...")
        
        return success, response

    def test_progress_update(self):
        """Test progress tracking update"""
        progress_data = {
            "player_id": "test_player_123",
            "level_id": 1,
            "action": "component_added",
            "component": "neural_layer",
            "timestamp": datetime.now().isoformat()
        }
        
        success, response = self.run_test(
            "Update Progress",
            "POST",
            "api/progress/update",
            200,
            data=progress_data,
            expected_fields=["success", "message"]
        )
        
        return success, response

    def test_get_progress(self):
        """Test getting player progress analytics"""
        success, response = self.run_test(
            "Get Player Progress",
            "GET",
            "api/progress/test_player_123",
            200,
            expected_fields=["player_id", "analytics"]
        )
        
        if success:
            analytics = response.get("analytics", {})
            print(f"   ✓ Analytics keys: {list(analytics.keys())}")
        
        return success, response

    def test_level_2_simulation(self):
        """Test Level 2 simulation with multiple components"""
        build_data = {
            "components": [
                {"name": "Neural Layer", "type": "layer", "id": "neural_layer"},
                {"name": "Activation Function", "type": "function", "id": "activation_relu"},
                {"name": "Dense Layer", "type": "layer", "id": "dense_layer"}
            ],
            "level_id": 2
        }
        
        success, response = self.run_test(
            "Level 2 Simulation",
            "POST",
            "api/simulate-build",
            200,
            data=build_data,
            expected_fields=["success", "score", "message"]
        )
        
        if success:
            score = response.get("score", 0)
            print(f"   ✓ Simulation score: {score:.2%}")
            
            if "educational_feedback" in response:
                print("   ✓ Educational feedback included")
            
            if "visual_data" in response:
                print("   ✓ Visual data included")
        
        return success, response

    def test_level_4_simulation(self):
        """Test Level 4 mini-boss simulation"""
        build_data = {
            "components": [
                {"name": "Neural Layer", "type": "layer", "id": "neural_layer"},
                {"name": "Activation Function", "type": "function", "id": "activation_relu"},
                {"name": "Dense Layer", "type": "layer", "id": "dense_layer"},
                {"name": "Dropout", "type": "regularization", "id": "dropout"}
            ],
            "level_id": 4
        }
        
        success, response = self.run_test(
            "Level 4 Mini-Boss Simulation",
            "POST",
            "api/simulate-build",
            200,
            data=build_data,
            expected_fields=["success", "score", "message"]
        )
        
        if success:
            score = response.get("score", 0)
            print(f"   ✓ Mini-boss score: {score:.2%}")
        
        return success, response

    def run_all_tests(self):
        """Run all enhanced API tests"""
        print("🚀 Starting Enhanced Tensor Forge API Tests")
        print("=" * 60)
        
        # Test core endpoints
        self.test_health_check()
        self.test_get_components()
        
        # Test level endpoints
        self.test_get_level_2()
        self.test_get_level_4()
        
        # Test enhanced features
        self.test_hint_system()
        self.test_progress_update()
        self.test_get_progress()
        
        # Test level-specific simulations
        self.test_level_2_simulation()
        self.test_level_4_simulation()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 ENHANCED TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 All enhanced tests passed! Backend API is fully functional.")
            return 0
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} test(s) failed. Check the issues above.")
            return 1

def main():
    """Main test runner"""
    base_url = "https://472b03e2-49c6-4e1d-a49b-f4a6b3bcb67a.preview.emergentagent.com"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing Enhanced Tensor Forge API at: {base_url}")
    
    tester = EnhancedTensorForgeAPITester(base_url)
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())