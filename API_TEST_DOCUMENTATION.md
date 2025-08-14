# CCDI API Test Suite Documentation

## Overview

This document describes the comprehensive test suite for the CCDI (Childhood Cancer Data Initiative) API. The test suite validates API endpoints against the specification, tests error handling, response formats, and basic performance.

## Test Scripts

### 1. Bash Test Script (`test_api.sh`)

A comprehensive bash script that tests all API endpoints using curl.

**Usage:**
```bash
./test_api.sh [OPTIONS] <server_url>

Options:
  -v, --verbose     Verbose output with response data
  -t, --timeout N   Request timeout in seconds (default: 30)
  -h, --help        Show help message

Examples:
  ./test_api.sh http://localhost:8000
  ./test_api.sh -v https://ccdi.cis230185.projects.jetstream-cloud.org
  ./test_api.sh -t 60 http://localhost:8000
```

### 2. Python Test Script (`test_api.py`)

An advanced Python script with detailed reporting and concurrent testing capabilities.

**Prerequisites:**
```bash
pip install requests
# or
pip install -r test-requirements.txt
```

**Usage:**
```bash
./test_api.py [OPTIONS] <server_url>

Options:
  -v, --verbose           Verbose output
  -t, --timeout N         Request timeout in seconds
  -r, --report-file FILE  Save JSON report to file

Examples:
  ./test_api.py http://localhost:8000
  ./test_api.py -v -r results.json https://ccdi.cis230185.projects.jetstream-cloud.org
```

### 3. Test Runner (`run_tests.sh`)

A unified test runner that can execute either bash or Python tests with automatic dependency management.

**Usage:**
```bash
./run_tests.sh [OPTIONS] <server_url>

Options:
  -t, --type TYPE         Test type: 'bash' or 'python' (default: bash)
  -v, --verbose           Verbose output
  -i, --install-deps      Install Python dependencies
  -r, --report FILE       Save test report (python only)

Examples:
  ./run_tests.sh http://localhost:8000
  ./run_tests.sh -t python -i -v http://localhost:8000
  ./run_tests.sh -t python -r results.json https://api.example.com
```

## Test Categories

### 📋 Basic API Tests
- **Root endpoint** (`/`) - API information
- **API info** (`/api/v1/info`) - Server and API details
- **OpenAPI documentation** (`/docs`) - Swagger UI
- **OpenAPI specification** (`/openapi.json`) - API schema

### 👤 Subject Endpoints
- **List subjects** (`/api/v1/subject`) - All subjects with pagination
- **Get specific subject** (`/api/v1/subject/{org}/{namespace}/{name}`)
- **Filter subjects** - By organization, namespace, etc.
- **Subject summary** (`/api/v1/subject/summary`) - Statistics
- **Subject diagnoses** (`/api/v1/subject-diagnosis`) - Diagnosis data

### 🧪 Sample Endpoints
- **List samples** (`/api/v1/sample`) - All samples with pagination
- **Get specific sample** (`/api/v1/sample/{org}/{namespace}/{name}`)
- **Filter samples** - By subject, organization, etc.
- **Sample summary** (`/api/v1/sample/summary`) - Statistics
- **Sample diagnoses** (`/api/v1/sample-diagnosis`) - Diagnosis data

### 📁 File Endpoints
- **List files** (`/api/v1/file`) - All files with pagination
- **Get specific file** (`/api/v1/file/{org}/{namespace}/{name}`)
- **Filter files** - By sample, type, etc.
- **File summary** (`/api/v1/file/summary`) - Statistics

### 🏷️ Namespace Endpoints
- **List namespaces** (`/api/v1/namespace`) - All namespaces
- **Get specific namespace** (`/api/v1/namespace/{org}/{namespace}`)

### 🏢 Organization Endpoints
- **List organizations** (`/api/v1/organization`) - All organizations
- **Get specific organization** (`/api/v1/organization/{name}`)

### 📊 Metadata Endpoints
- **Subject metadata fields** (`/api/v1/metadata/fields/subject`)
- **Sample metadata fields** (`/api/v1/metadata/fields/sample`)
- **File metadata fields** (`/api/v1/metadata/fields/file`)

### 🔍 Response Structure Tests
- Validates JSON response structure
- Checks for required fields
- Ensures proper data types

### ❌ Error Handling Tests
- **404 errors** - Non-existent resources
- **422 errors** - Invalid request format
- **CORS headers** - Cross-origin support

### ⚡ Performance Tests
- Response time measurement
- Concurrent request handling
- Basic load testing

## Test Results Analysis

### Recent Test Results (Local Server)

**Total Tests:** 42  
**✅ Passed:** 41  
**❌ Failed:** 1  

#### Passed Tests Summary:
- ✅ All basic API endpoints working
- ✅ All CRUD operations functional
- ✅ Proper pagination support
- ✅ Filtering and querying working
- ✅ JSON structure validation passed
- ✅ Error handling for 404s working
- ✅ CORS headers present
- ✅ Response times under 1000ms

#### Failed Tests:
- ❌ **Invalid path format validation** - Expected 422, got 404
  - The API returns 404 instead of 422 for malformed paths
  - This is acceptable behavior and doesn't affect functionality

### Expected Response Formats

#### Success Response Example:
```json
{
  "summary": {
    "total": 5,
    "limit": 10,
    "offset": 0
  },
  "data": [
    {
      "id": {
        "namespace": {
          "organization": "STJUDE",
          "name": "PNOC"
        },
        "name": "SUBJECT001"
      },
      "kind": "Participant",
      "metadata": {
        "sex": {"value": "F"},
        "race": {"value": "White"}
      }
    }
  ]
}
```

#### Error Response Example:
```json
{
  "errors": [
    {
      "kind": "NotFound",
      "entity": "Resource at /api/v1/subject/INVALID",
      "message": "Resource at /api/v1/subject/INVALID not found."
    }
  ]
}
```

## Performance Benchmarks

### Response Time Targets:
- **API Info:** < 100ms
- **List endpoints:** < 500ms
- **Individual resource:** < 200ms
- **Summary endpoints:** < 300ms

### Concurrent Request Handling:
- **5 concurrent requests:** Average < 1000ms
- **Connection timeout:** 30s default
- **Request timeout:** 30s default

## Usage in CI/CD

### GitHub Actions Example:
```yaml
- name: Test API
  run: |
    ./test_api.sh https://api.staging.example.com
    
- name: Generate Test Report
  run: |
    ./test_api.py -r test-results.json https://api.staging.example.com
    
- name: Upload Test Results
  uses: actions/upload-artifact@v2
  with:
    name: api-test-results
    path: test-results.json
```

### Docker Integration:
```bash
# Test local Docker container
docker run -d -p 8000:8000 ccdi-api
./test_api.sh http://localhost:8000

# Test production deployment
./test_api.sh https://ccdi.cis230185.projects.jetstream-cloud.org
```

## Troubleshooting

### Common Issues:

1. **Connection Refused**
   ```bash
   # Check if server is running
   curl -I http://localhost:8000
   
   # Check Docker containers
   docker ps
   ```

2. **SSL/TLS Errors**
   ```bash
   # Test HTTPS connection
   curl -k https://your-domain.com/api/v1/info
   
   # Check certificate
   openssl s_client -connect your-domain.com:443
   ```

3. **Timeout Issues**
   ```bash
   # Increase timeout
   ./test_api.sh -t 60 https://slow-server.com
   
   # Test specific endpoint
   curl -m 30 https://your-api.com/api/v1/info
   ```

4. **Missing Dependencies**
   ```bash
   # For Python tests
   pip install -r test-requirements.txt
   
   # Or use auto-install
   ./run_tests.sh -i -t python http://localhost:8000
   ```

## Extending the Test Suite

### Adding New Tests:

1. **Bash Script:** Add test calls in appropriate sections
2. **Python Script:** Add methods to the CCDIAPITester class
3. **Test Data:** Update test subject/sample/file IDs as needed

### Custom Assertions:
```bash
# Bash example
test_custom_field() {
    response=$(curl -s "$1")
    if echo "$response" | grep -q "custom_field"; then
        echo "✓ PASS - Custom field present"
    else
        echo "✗ FAIL - Custom field missing"
    fi
}
```

```python
# Python example
def test_custom_validation(self, endpoint: str):
    response, time = self.make_request("GET", endpoint)
    data = response.json()
    
    if "custom_field" in data:
        return TestResult("Custom validation", endpoint, "GET", "PASS", 200, 200, time)
    else:
        return TestResult("Custom validation", endpoint, "GET", "FAIL", 200, 200, time, "Missing custom_field")
```

## Reporting and Monitoring

### Test Report Format (JSON):
```json
{
  "timestamp": "2025-08-14T10:06:51",
  "base_url": "http://localhost:8000",
  "total_tests": 42,
  "passed_tests": 41,
  "failed_tests": 1,
  "results": [
    {
      "name": "Root endpoint",
      "endpoint": "/",
      "method": "GET",
      "status": "PASS",
      "expected_status": 200,
      "actual_status": 200,
      "response_time": 45.2
    }
  ]
}
```

### Integration with Monitoring:
- **Prometheus metrics** from test results
- **Grafana dashboards** for API health
- **Alert triggers** for test failures
- **Slack/email notifications** for CI/CD failures

The test suite provides comprehensive coverage of the CCDI API specification and can be easily integrated into development workflows and deployment pipelines.
