#!/bin/bash

# CCDI API Production Deployment Script with Nginx

set -e

echo "🚀 Deploying CCDI API with Nginx reverse proxy..."

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Health check
echo "Performing health check..."
if curl -f http://localhost/api/v1/info > /dev/null 2>&1; then
    echo "✅ CCDI API is running successfully!"
    echo ""
    echo "🌐 API Access Points:"
    echo "  Main API: http://localhost"
    echo "  API Info: http://localhost/api/v1/info"
    echo "  Swagger Docs: http://localhost/docs"
    echo "  API Endpoints: http://localhost/api/v1/{endpoint}"
    echo ""
    echo "🔧 Management Commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop services: docker-compose down"
    echo "  Restart: docker-compose restart"
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
else
    echo "❌ Health check failed!"
    echo "Checking logs..."
    docker-compose logs
    exit 1
fi
