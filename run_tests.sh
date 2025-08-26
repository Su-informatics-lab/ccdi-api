#!/bin/bash

# CCDI API Test Runner
# Handles setup and runs API tests with multiple options

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
SERVER_URL=""
TEST_TYPE="bash"  # bash or python
INSTALL_DEPS=false
VERBOSE=false
REPORT_FILE=""

usage() {
    echo "Usage: $0 [OPTIONS] <server_url>"
    echo ""
    echo "Run CCDI API specification tests"
    echo ""
    echo "Arguments:"
    echo "  server_url              Base URL of the API server"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE         Test type: 'bash' or 'python' (default: bash)"
    echo "  -v, --verbose           Verbose output"
    echo "  -i, --install-deps      Install Python dependencies (for python tests)"
    echo "  -r, --report FILE       Save test report to file (python tests only)"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 http://localhost:8000"
    echo "  $0 -t python -v https://ccdi.ipo.sulab.io"
    echo "  $0 -t python -i -r results.json http://localhost:8000"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -i|--install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        -r|--report)
            REPORT_FILE="$2"
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

if [ -z "$SERVER_URL" ]; then
    echo -e "${RED}Error: Server URL is required${NC}"
    usage
    exit 1
fi

if [ "$TEST_TYPE" != "bash" ] && [ "$TEST_TYPE" != "python" ]; then
    echo -e "${RED}Error: Test type must be 'bash' or 'python'${NC}"
    exit 1
fi

echo -e "${BLUE}🧪 CCDI API Test Runner${NC}"
echo -e "${BLUE}========================${NC}"
echo "Server URL: $SERVER_URL"
echo "Test Type: $TEST_TYPE"
echo "Verbose: $VERBOSE"
echo ""

# Install Python dependencies if requested
if [ "$TEST_TYPE" = "python" ] && [ "$INSTALL_DEPS" = true ]; then
    echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
    if command -v pip3 &> /dev/null; then
        pip3 install -r test-requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r test-requirements.txt
    else
        echo -e "${RED}Error: pip not found. Please install Python pip.${NC}"
        exit 1
    fi
    echo ""
fi

# Run tests based on type
if [ "$TEST_TYPE" = "bash" ]; then
    echo -e "${GREEN}🚀 Running Bash test suite...${NC}"
    if [ "$VERBOSE" = true ]; then
        ./test_api.sh --verbose "$SERVER_URL"
    else
        ./test_api.sh "$SERVER_URL"
    fi
    
elif [ "$TEST_TYPE" = "python" ]; then
    echo -e "${GREEN}🚀 Running Python test suite...${NC}"
    
    # Check if requests is available
    if ! python3 -c "import requests" 2>/dev/null; then
        echo -e "${YELLOW}⚠️ Warning: requests library not found${NC}"
        echo "Install with: pip3 install requests"
        echo "Or run with: $0 -i -t python $SERVER_URL"
        echo ""
    fi
    
    # Build Python command
    python_cmd="python3 test_api.py"
    
    if [ "$VERBOSE" = true ]; then
        python_cmd="$python_cmd --verbose"
    fi
    
    if [ -n "$REPORT_FILE" ]; then
        python_cmd="$python_cmd --report-file $REPORT_FILE"
    fi
    
    python_cmd="$python_cmd $SERVER_URL"
    
    # Execute Python tests
    eval $python_cmd
fi
