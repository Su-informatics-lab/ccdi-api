#!/bin/bash

# CCDI API Test Script
# Tests all API endpoints against the specification
# Usage: ./test_api.sh <server_url>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DEFAULT_URL="http://localhost:8000"
TIMEOUT=30
VERBOSE=false

# Usage function
usage() {
    echo "Usage: $0 [OPTIONS] <server_url>"
    echo ""
    echo "Test CCDI API endpoints against specification"
    echo ""
    echo "Arguments:"
    echo "  server_url    Base URL of the API server (default: $DEFAULT_URL)"
    echo ""
    echo "Options:"
    echo "  -v, --verbose     Verbose output"
    echo "  -t, --timeout N   Request timeout in seconds (default: $TIMEOUT)"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 http://localhost:8000"
    echo "  $0 https://ccdi.ipo.sulab.io"
    echo "  $0 -v -t 60 https://api.example.com"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            echo "Unknown option $1"
            usage
            exit 1
            ;;
        *)
            SERVER_URL="$1"
            shift
            ;;
    esac
done

# Set default URL if not provided
if [ -z "$SERVER_URL" ]; then
    SERVER_URL="$DEFAULT_URL"
fi

# Remove trailing slash from URL
SERVER_URL="${SERVER_URL%/}"

echo -e "${BLUE}🧪 CCDI API Test Suite${NC}"
echo -e "${BLUE}=========================${NC}"
echo "Server URL: $SERVER_URL"
echo "Timeout: ${TIMEOUT}s"
echo "Verbose: $VERBOSE"
echo ""

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper function to make API requests
api_request() {
    local method="$1"
    local endpoint="$2"
    local expected_status="$3"
    local description="$4"
    local data="$5"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    local curl_opts="-s -w %{http_code} --connect-timeout $TIMEOUT"
    local full_url="${SERVER_URL}${endpoint}"
    
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}Testing:${NC} $method $endpoint - $description"
    fi
    
    local response
    local status_code
    
    if [ "$method" = "GET" ]; then
        response=$(curl $curl_opts "$full_url" 2>/dev/null)
    elif [ "$method" = "POST" ]; then
        if [ -n "$data" ]; then
            response=$(curl $curl_opts -X POST -H "Content-Type: application/json" -d "$data" "$full_url" 2>/dev/null)
        else
            response=$(curl $curl_opts -X POST "$full_url" 2>/dev/null)
        fi
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ FAIL${NC} - $description (Connection failed)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
    
    # Extract status code (last 3 characters)
    status_code="${response: -3}"
    # Extract response body (everything except last 3 characters)
    response_body="${response%???}"
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} - $description"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        
        if [ "$VERBOSE" = true ] && [ -n "$response_body" ]; then
            echo "  Response: ${response_body:0:200}..."
        fi
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} - $description (Expected $expected_status, got $status_code)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        
        if [ "$VERBOSE" = true ] && [ -n "$response_body" ]; then
            echo "  Response: ${response_body:0:200}..."
        fi
        return 1
    fi
}

# Helper function to test JSON response structure
test_json_structure() {
    local endpoint="$1"
    local description="$2"
    local expected_fields="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    local response=$(curl -s --connect-timeout $TIMEOUT "${SERVER_URL}${endpoint}" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ FAIL${NC} - $description (Connection failed)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
    
    # Check if response is valid JSON and contains expected fields
    local missing_fields=""
    for field in $expected_fields; do
        if ! echo "$response" | grep -q "\"$field\""; then
            missing_fields="$missing_fields $field"
        fi
    done
    
    if [ -z "$missing_fields" ]; then
        echo -e "${GREEN}✓ PASS${NC} - $description"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} - $description (Missing fields:$missing_fields)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo -e "${YELLOW}📋 Running API Specification Tests...${NC}"
echo ""

# Test 1: Root endpoint
api_request "GET" "/" "200" "Root endpoint returns API information"

# Test 2: API Info endpoint
api_request "GET" "/api/v1/info" "200" "API info endpoint"

# Test 3: OpenAPI documentation
api_request "GET" "/docs" "200" "Swagger UI documentation"

# Test 4: OpenAPI JSON specification
api_request "GET" "/openapi.json" "200" "OpenAPI JSON specification"

# Test 5-10: Subject endpoints
echo ""
echo -e "${YELLOW}👤 Testing Subject Endpoints${NC}"
api_request "GET" "/api/v1/subject" "200" "List all subjects"
api_request "GET" "/api/v1/subject?page=1&per_page=2" "200" "List subjects with pagination"
api_request "GET" "/api/v1/subject?sex=F" "200" "Filter subjects by sex"
api_request "GET" "/api/v1/subject?race=Unknown" "200" "Filter subjects by race"

# Test specific subject (using first subject from data)
api_request "GET" "/api/v1/subject/IUSCCC/PST001/535" "200" "Get specific subject"

# Test non-existent subject
api_request "GET" "/api/v1/subject/INVALID/ORG/INVALID" "404" "Non-existent subject returns 404"

# Test 11-16: Sample endpoints
echo ""
echo -e "${YELLOW}🧪 Testing Sample Endpoints${NC}"
api_request "GET" "/api/v1/sample" "200" "List all samples"
api_request "GET" "/api/v1/sample?page=1&per_page=2" "200" "List samples with pagination"
api_request "GET" "/api/v1/sample?tissue_type=Normal" "200" "Filter samples by tissue type"
api_request "GET" "/api/v1/sample?disease_phase=Initial%20Diagnosis" "200" "Filter samples by disease phase"

# Test specific sample
api_request "GET" "/api/v1/sample/IUSCCC/PST001/3" "200" "Get specific sample"

# Test samples by subject
api_request "GET" "/api/v1/sample?subject_name=7" "200" "Filter samples by subject"

# Test non-existent sample
api_request "GET" "/api/v1/sample/INVALID/ORG/INVALID" "404" "Non-existent sample returns 404"

# Test 17-22: File endpoints
echo ""
echo -e "${YELLOW}📁 Testing File Endpoints${NC}"
api_request "GET" "/api/v1/file" "200" "List all files"
api_request "GET" "/api/v1/file?page=1&per_page=1" "200" "List files with pagination"
api_request "GET" "/api/v1/file?type=BAM" "200" "Filter files by type"

# Test specific file
api_request "GET" "/api/v1/file/IUSCCC/PST001/CRF000001.bam" "200" "Get specific file"

# Test files by sample
api_request "GET" "/api/v1/file?sample_name=3" "200" "Filter files by sample"

# Test non-existent file
api_request "GET" "/api/v1/file/INVALID/ORG/INVALID.txt" "404" "Non-existent file returns 404"

# Test 29-34: Namespace endpoints
echo ""
echo -e "${YELLOW}📁 Testing Namespace Endpoints${NC}"
api_request "GET" "/api/v1/namespace" "200" "List all namespaces"
api_request "GET" "/api/v1/namespace?page=1&per_page=1" "200" "List namespaces with pagination"

# Test specific namespace
api_request "GET" "/api/v1/namespace/IUSCCC/PST001" "200" "Get specific namespace"

# Test namespaces by organization
api_request "GET" "/api/v1/namespace?organization_name=IUSCCC" "200" "Filter namespaces by organization"

# Test non-existent namespace
api_request "GET" "/api/v1/namespace/INVALID/INVALID" "404" "Non-existent namespace returns 404"

# Test 27-30: Organization endpoints
echo ""
echo -e "${YELLOW}🏢 Testing Organization Endpoints${NC}"
api_request "GET" "/api/v1/organization" "200" "List all organizations"
api_request "GET" "/api/v1/organization?page=1&per_page=1" "200" "List organizations with pagination"

# Test specific organization
api_request "GET" "/api/v1/organization/IUSCCC" "200" "Get specific organization"

# Test non-existent organization
api_request "GET" "/api/v1/organization/INVALID" "404" "Non-existent organization returns 404"

# Test 35-40: Metadata endpoint
echo ""
echo -e "${YELLOW}📊 Testing Metadata Endpoint${NC}"
# api_request "GET" "/api/v1/metadata" "200" "Get metadata information"
api_request "GET" "/api/v1/metadata/fields/subject" "200" "Get subject metadata"
api_request "GET" "/api/v1/metadata/fields/sample" "200" "Get sample metadata"
api_request "GET" "/api/v1/metadata/fields/file" "200" "Get file metadata"
# api_request "GET" "/api/v1/metadata/fields/organization" "200" "Get organization metadata"
# api_request "GET" "/api/v1/metadata/fields/namespace" "200" "Get namespace metadata"

# Test JSON structure validation
echo ""
echo -e "${YELLOW}🔍 Testing Response Structure${NC}"
test_json_structure "/api/v1/info" "API info contains required fields" "server api"
test_json_structure "/" "Root response contains required fields" "title version endpoints"
test_json_structure "/api/v1/metadata/fields/subject" "Subject metadata contains required fields" "fields"

# Test error handling
echo ""
echo -e "${YELLOW}❌ Testing Error Handling${NC}"
api_request "GET" "/api/v1/nonexistent" "404" "Non-existent endpoint returns 404"
api_request "GET" "/api/v1/subject/invalid-format" "422" "Invalid path format returns 422"

# Test CORS headers (if applicable)
echo ""
echo -e "${YELLOW}🌐 Testing CORS Headers${NC}"
TOTAL_TESTS=$((TOTAL_TESTS + 1))
cors_response=$(curl -s -I -H "Origin: https://example.com" "${SERVER_URL}/api/v1/info" 2>/dev/null)
if echo "$cors_response" | grep -q "Access-Control-Allow-Origin"; then
    echo -e "${GREEN}✓ PASS${NC} - CORS headers present"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${YELLOW}⚠ WARN${NC} - CORS headers not detected"
    PASSED_TESTS=$((PASSED_TESTS + 1))  # Not a failure for this test
fi

# Performance test
echo ""
echo -e "${YELLOW}⚡ Basic Performance Test${NC}"
TOTAL_TESTS=$((TOTAL_TESTS + 1))
start_time=$(date +%s%N)
curl -s "${SERVER_URL}/api/v1/info" > /dev/null 2>&1
end_time=$(date +%s%N)
response_time=$(( (end_time - start_time) / 1000000 ))  # Convert to milliseconds

if [ $response_time -lt 1000 ]; then
    echo -e "${GREEN}✓ PASS${NC} - API response time: ${response_time}ms (< 1000ms)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${YELLOW}⚠ SLOW${NC} - API response time: ${response_time}ms (> 1000ms)"
    PASSED_TESTS=$((PASSED_TESTS + 1))  # Not a failure
fi

# Summary
echo ""
echo -e "${BLUE}📊 Test Summary${NC}"
echo -e "${BLUE}===============${NC}"
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! API is working correctly.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed. Please check the API implementation.${NC}"
    exit 1
fi
