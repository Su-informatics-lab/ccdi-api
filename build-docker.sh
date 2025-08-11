#!/bin/bash

# CCDI API Docker Build and Run Script

set -e

echo "🐳 Building CCDI API Docker image..."

# Build the Docker image
docker build -t ccdi-api .

echo "✅ Docker image built successfully!"

echo "🚀 Available commands:"
echo ""
echo "Run the container:"
echo "  docker run -d -p 8000:8000 --name ccdi-api-container ccdi-api"
echo ""
echo "Run with docker-compose:"
echo "  docker-compose up -d"
echo ""
echo "View logs:"
echo "  docker logs ccdi-api-container"
echo ""
echo "Stop and remove container:"
echo "  docker stop ccdi-api-container && docker rm ccdi-api-container"
echo ""
echo "Access the API:"
echo "  http://localhost:8000"
echo "  http://localhost:8000/docs (Swagger UI)"
echo "  http://localhost:8000/api/v1/info"
echo ""
echo "Test the API:"
echo "  curl http://localhost:8000/api/v1/info"
