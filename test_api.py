#!/usr/bin/env python3
"""
CCDI API Specification Test Suite

A comprehensive test suite to validate the CCDI API against its specification.
Tests all endpoints, response formats, error handling, and performance.

Usage:
    python test_api.py <server_url> [options]

Examples:
    python test_api.py http://localhost:8000
    python test_api.py https://ccdi.cis230185.projects.jetstream-cloud.org --verbose
    python test_api.py http://localhost:8000 --timeout 60 --report-file results.json
"""

import argparse
import json
import sys
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin
import concurrent.futures


@dataclass
class TestResult:
    """Test result data structure"""
    name: str
    endpoint: str
    method: str
    status: str  # PASS, FAIL, SKIP
    expected_status: int
    actual_status: int
    response_time: float
    error_message: Optional[str] = None
    response_data: Optional[Dict] = None


class CCDIAPITester:
    """CCDI API Test Suite"""
    
    def __init__(self, base_url: str, timeout: int = 30, verbose: bool = False):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verbose = verbose
        self.session = requests.Session()
        self.session.timeout = timeout
        self.results: List[TestResult] = []
        
        # Test data from the API specification
        self.test_subjects = ["STJUDE/PNOC/SUBJECT001", "TREEHOUSE/COMPBIO/SUBJECT002"]
        self.test_samples = ["STJUDE/PNOC/SAMPLE001", "TREEHOUSE/COMPBIO/SAMPLE002"]
        self.test_files = ["STJUDE/PNOC/RNASeq_001.fastq.gz", "TREEHOUSE/COMPBIO/WGS_002.bam"]
        self.test_namespaces = ["STJUDE/PNOC", "TREEHOUSE/COMPBIO"]
        self.test_organizations = ["STJUDE", "TREEHOUSE", "COG"]
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "ERROR":
            print(f"[{timestamp}] ❌ {message}")
        elif level == "SUCCESS":
            print(f"[{timestamp}] ✅ {message}")
        elif level == "WARNING":
            print(f"[{timestamp}] ⚠️  {message}")
        elif self.verbose or level in ["ERROR", "SUCCESS"]:
            print(f"[{timestamp}] ℹ️  {message}")
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """Make HTTP request and measure response time"""
        url = urljoin(self.base_url, endpoint)
        
        start_time = time.time()
        try:
            response = self.session.request(method, url, **kwargs)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            return response, response_time
        except requests.RequestException as e:
            response_time = (time.time() - start_time) * 1000
            raise e
    
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     expected_status: int = 200, **request_kwargs) -> TestResult:
        """Test a single endpoint"""
        self.log(f"Testing {method} {endpoint} - {name}")
        
        try:
            response, response_time = self.make_request(method, endpoint, **request_kwargs)
            
            # Parse response data if JSON
            response_data = None
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    response_data = response.json()
            except json.JSONDecodeError:
                pass
            
            # Determine test status
            status = "PASS" if response.status_code == expected_status else "FAIL"
            error_message = None if status == "PASS" else f"Expected {expected_status}, got {response.status_code}"
            
            result = TestResult(
                name=name,
                endpoint=endpoint,
                method=method,
                status=status,
                expected_status=expected_status,
                actual_status=response.status_code,
                response_time=response_time,
                error_message=error_message,
                response_data=response_data
            )
            
            if status == "PASS":
                self.log(f"✓ {name} ({response_time:.1f}ms)", "SUCCESS")
            else:
                self.log(f"✗ {name} - {error_message} ({response_time:.1f}ms)", "ERROR")
            
            return result
            
        except requests.RequestException as e:
            result = TestResult(
                name=name,
                endpoint=endpoint,
                method=method,
                status="FAIL",
                expected_status=expected_status,
                actual_status=0,
                response_time=0,
                error_message=str(e)
            )
            
            self.log(f"✗ {name} - Connection error: {e}", "ERROR")
            return result
    
    def test_json_structure(self, name: str, endpoint: str, required_fields: List[str]) -> TestResult:
        """Test JSON response structure"""
        self.log(f"Testing JSON structure for {endpoint} - {name}")
        
        try:
            response, response_time = self.make_request("GET", endpoint)
            
            if response.status_code != 200:
                return TestResult(
                    name=name,
                    endpoint=endpoint,
                    method="GET",
                    status="FAIL",
                    expected_status=200,
                    actual_status=response.status_code,
                    response_time=response_time,
                    error_message=f"HTTP {response.status_code}"
                )
            
            try:
                data = response.json()
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    error_message = f"Missing required fields: {', '.join(missing_fields)}"
                    status = "FAIL"
                    self.log(f"✗ {name} - {error_message}", "ERROR")
                else:
                    error_message = None
                    status = "PASS"
                    self.log(f"✓ {name} - All required fields present", "SUCCESS")
                
                return TestResult(
                    name=name,
                    endpoint=endpoint,
                    method="GET",
                    status=status,
                    expected_status=200,
                    actual_status=200,
                    response_time=response_time,
                    error_message=error_message,
                    response_data=data
                )
                
            except json.JSONDecodeError:
                return TestResult(
                    name=name,
                    endpoint=endpoint,
                    method="GET",
                    status="FAIL",
                    expected_status=200,
                    actual_status=200,
                    response_time=response_time,
                    error_message="Invalid JSON response"
                )
                
        except requests.RequestException as e:
            return TestResult(
                name=name,
                endpoint=endpoint,
                method="GET",
                status="FAIL",
                expected_status=200,
                actual_status=0,
                response_time=0,
                error_message=str(e)
            )
    
    def run_basic_tests(self):
        """Run basic API tests"""
        self.log("🧪 Running Basic API Tests")
        
        tests = [
            ("Root endpoint", "GET", "/", 200),
            ("API info endpoint", "GET", "/api/v1/info", 200),
            ("OpenAPI documentation", "GET", "/docs", 200),
            ("OpenAPI JSON spec", "GET", "/openapi.json", 200),
        ]
        
        for name, method, endpoint, expected_status in tests:
            result = self.test_endpoint(name, method, endpoint, expected_status)
            self.results.append(result)
    
    def run_subject_tests(self):
        """Run subject endpoint tests"""
        self.log("👤 Running Subject Tests")
        
        # Basic subject tests
        tests = [
            ("List all subjects", "GET", "/api/v1/subject", 200),
            ("List subjects with limit", "GET", "/api/v1/subject?limit=2", 200),
            ("List subjects with offset", "GET", "/api/v1/subject?offset=1", 200),
            ("Filter subjects by organization", "GET", "/api/v1/subject?namespace_organization=STJUDE", 200),
        ]
        
        for name, method, endpoint, expected_status in tests:
            result = self.test_endpoint(name, method, endpoint, expected_status)
            self.results.append(result)
        
        # Test specific subjects
        for subject_id in self.test_subjects:
            result = self.test_endpoint(
                f"Get subject {subject_id}",
                "GET",
                f"/api/v1/subject/{subject_id}",
                200
            )
            self.results.append(result)
        
        # Test non-existent subject
        result = self.test_endpoint(
            "Non-existent subject returns 404",
            "GET",
            "/api/v1/subject/INVALID/ORG/INVALID",
            404
        )
        self.results.append(result)
    
    def run_sample_tests(self):
        """Run sample endpoint tests"""
        self.log("🧪 Running Sample Tests")
        
        tests = [
            ("List all samples", "GET", "/api/v1/sample", 200),
            ("List samples with limit", "GET", "/api/v1/sample?limit=2", 200),
            ("Filter samples by subject", "GET", "/api/v1/sample?subject_name=SUBJECT001", 200),
        ]
        
        for name, method, endpoint, expected_status in tests:
            result = self.test_endpoint(name, method, endpoint, expected_status)
            self.results.append(result)
        
        # Test specific samples
        for sample_id in self.test_samples:
            result = self.test_endpoint(
                f"Get sample {sample_id}",
                "GET",
                f"/api/v1/sample/{sample_id}",
                200
            )
            self.results.append(result)
        
        # Test non-existent sample
        result = self.test_endpoint(
            "Non-existent sample returns 404",
            "GET",
            "/api/v1/sample/INVALID/ORG/INVALID",
            404
        )
        self.results.append(result)
    
    def run_file_tests(self):
        """Run file endpoint tests"""
        self.log("📁 Running File Tests")
        
        tests = [
            ("List all files", "GET", "/api/v1/file", 200),
            ("List files with limit", "GET", "/api/v1/file?limit=1", 200),
            ("Filter files by sample", "GET", "/api/v1/file?sample_name=SAMPLE001", 200),
        ]
        
        for name, method, endpoint, expected_status in tests:
            result = self.test_endpoint(name, method, endpoint, expected_status)
            self.results.append(result)
        
        # Test specific files
        for file_id in self.test_files:
            result = self.test_endpoint(
                f"Get file {file_id}",
                "GET",
                f"/api/v1/file/{file_id}",
                200
            )
            self.results.append(result)
    
    def run_namespace_tests(self):
        """Run namespace endpoint tests"""
        self.log("🏷️ Running Namespace Tests")
        
        # List all namespaces
        result = self.test_endpoint("List all namespaces", "GET", "/api/v1/namespace", 200)
        self.results.append(result)
        
        # Test specific namespaces
        for namespace_id in self.test_namespaces:
            result = self.test_endpoint(
                f"Get namespace {namespace_id}",
                "GET",
                f"/api/v1/namespace/{namespace_id}",
                200
            )
            self.results.append(result)
    
    def run_organization_tests(self):
        """Run organization endpoint tests"""
        self.log("🏢 Running Organization Tests")
        
        # List all organizations
        result = self.test_endpoint("List all organizations", "GET", "/api/v1/organization", 200)
        self.results.append(result)
        
        # Test specific organizations
        for org_id in self.test_organizations:
            result = self.test_endpoint(
                f"Get organization {org_id}",
                "GET",
                f"/api/v1/organization/{org_id}",
                200
            )
            self.results.append(result)
    
    def run_metadata_tests(self):
        """Run metadata endpoint tests"""
        self.log("📊 Running Metadata Tests")
        
        tests = [
            ("Get subject metadata fields", "GET", "/api/v1/metadata/fields/subject", 200),
            ("Get sample metadata fields", "GET", "/api/v1/metadata/fields/sample", 200),
            ("Get file metadata fields", "GET", "/api/v1/metadata/fields/file", 200),
            ("Get subject summary", "GET", "/api/v1/subject/summary", 200),
            ("Get sample summary", "GET", "/api/v1/sample/summary", 200),
            ("Get file summary", "GET", "/api/v1/file/summary", 200),
            ("Get subject diagnoses", "GET", "/api/v1/subject-diagnosis", 200),
            ("Get sample diagnoses", "GET", "/api/v1/sample-diagnosis", 200),
        ]
        
        for name, method, endpoint, expected_status in tests:
            result = self.test_endpoint(name, method, endpoint, expected_status)
            self.results.append(result)
    
    def run_structure_tests(self):
        """Run JSON structure validation tests"""
        self.log("🔍 Running Structure Validation Tests")
        
        structure_tests = [
            ("API info structure", "/api/v1/info", ["server", "api"]),
            ("Root response structure", "/", ["title", "version", "endpoints"]),
            ("Subject metadata structure", "/api/v1/metadata/fields/subject", ["fields"]),
            ("Subject summary structure", "/api/v1/subject/summary", ["total"]),
        ]
        
        for name, endpoint, required_fields in structure_tests:
            result = self.test_json_structure(name, endpoint, required_fields)
            self.results.append(result)
    
    def run_error_tests(self):
        """Run error handling tests"""
        self.log("❌ Running Error Handling Tests")
        
        error_tests = [
            ("Non-existent endpoint returns 404", "GET", "/api/v1/nonexistent", 404),
            ("Invalid path format", "GET", "/api/v1/subject/invalid-format", 422),
        ]
        
        for name, method, endpoint, expected_status in error_tests:
            result = self.test_endpoint(name, method, endpoint, expected_status)
            self.results.append(result)
    
    def run_performance_tests(self):
        """Run basic performance tests"""
        self.log("⚡ Running Performance Tests")
        
        # Test multiple concurrent requests
        def concurrent_request():
            try:
                response, response_time = self.make_request("GET", "/api/v1/info")
                return response_time
            except:
                return None
        
        # Run 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(concurrent_request) for _ in range(5)]
            response_times = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        valid_times = [t for t in response_times if t is not None]
        if valid_times:
            avg_response_time = sum(valid_times) / len(valid_times)
            max_response_time = max(valid_times)
            
            self.log(f"Concurrent requests - Avg: {avg_response_time:.1f}ms, Max: {max_response_time:.1f}ms")
            
            # Create performance result
            status = "PASS" if avg_response_time < 1000 else "WARNING"
            result = TestResult(
                name="Concurrent request performance",
                endpoint="/api/v1/info",
                method="GET",
                status=status,
                expected_status=200,
                actual_status=200,
                response_time=avg_response_time,
                error_message=None if status == "PASS" else f"Average response time {avg_response_time:.1f}ms > 1000ms"
            )
            self.results.append(result)
    
    def run_all_tests(self):
        """Run complete test suite"""
        start_time = time.time()
        
        print(f"🧪 CCDI API Test Suite")
        print(f"======================")
        print(f"Server URL: {self.base_url}")
        print(f"Timeout: {self.timeout}s")
        print(f"Verbose: {self.verbose}")
        print()
        
        try:
            self.run_basic_tests()
            self.run_subject_tests()
            self.run_sample_tests()
            self.run_file_tests()
            self.run_namespace_tests()
            self.run_organization_tests()
            self.run_metadata_tests()
            self.run_structure_tests()
            self.run_error_tests()
            self.run_performance_tests()
            
        except KeyboardInterrupt:
            self.log("Test suite interrupted by user", "WARNING")
        
        total_time = time.time() - start_time
        self.print_summary(total_time)
    
    def print_summary(self, total_time: float):
        """Print test summary"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "PASS"])
        failed_tests = len([r for r in self.results if r.status == "FAIL"])
        
        print()
        print("📊 Test Summary")
        print("===============")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏱️ Total Time: {total_time:.2f}s")
        
        if failed_tests > 0:
            print()
            print("❌ Failed Tests:")
            for result in self.results:
                if result.status == "FAIL":
                    print(f"  • {result.name}: {result.error_message}")
        
        # Calculate average response time
        response_times = [r.response_time for r in self.results if r.response_time > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"📈 Average Response Time: {avg_response_time:.1f}ms")
        
        print()
        if failed_tests == 0:
            print("🎉 All tests passed! API is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Please check the API implementation.")
            return False
    
    def save_report(self, filename: str):
        """Save test results to JSON file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_tests": len(self.results),
            "passed_tests": len([r for r in self.results if r.status == "PASS"]),
            "failed_tests": len([r for r in self.results if r.status == "FAIL"]),
            "results": [asdict(result) for result in self.results]
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Test report saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="CCDI API Test Suite")
    parser.add_argument("server_url", help="Base URL of the API server")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Request timeout in seconds")
    parser.add_argument("-r", "--report-file", help="Save test report to JSON file")
    
    args = parser.parse_args()
    
    # Create and run test suite
    tester = CCDIAPITester(args.server_url, args.timeout, args.verbose)
    tester.run_all_tests()
    
    # Save report if requested
    if args.report_file:
        tester.save_report(args.report_file)
    
    # Exit with appropriate code
    failed_tests = len([r for r in tester.results if r.status == "FAIL"])
    sys.exit(0 if failed_tests == 0 else 1)


if __name__ == "__main__":
    main()
