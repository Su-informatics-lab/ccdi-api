#!/bin/bash

# SSL Deployment Script
set -e

echo "Deploying CCDI API with SSL..."

# Check if certificates exist
if [ ! -d "/etc/letsencrypt/live" ]; then
    echo "Error: SSL certificates not found!"
    echo "Please run ./setup-ssl.sh first"
    exit 1
fi

# Stop existing containers
docker-compose down

# Build and start with SSL profile
docker-compose --profile ssl up --build -d

echo "Services starting..."
sleep 10

# Check service status
docker-compose ps

echo ""
echo "✅ CCDI API deployed with SSL!"
echo "🔒 HTTPS: https://your-domain.com"
echo "📊 API Info: https://your-domain.com/api/v1/info"
echo "📖 Docs: https://your-domain.com/docs"
echo ""
echo "Certificate auto-renewal is configured via certbot container"