#!/bin/bash

# CCDI API SSL Deployment Script
# Domain: ccdi.cis230185.projects.jetstream-cloud.org

set -e

DOMAIN="ccdi.cis230185.projects.jetstream-cloud.org"

echo "🚀 Deploying CCDI API with SSL for $DOMAIN..."

# Check if certificates exist
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    echo "❌ Error: SSL certificates not found for $DOMAIN!"
    echo "Please run ./setup_ssl.sh first"
    exit 1
fi

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose_ssl.yml down 2>/dev/null || true

# Build and start with SSL
echo "Building and starting services with SSL..."
docker-compose -f docker-compose_ssl.yml up --build -d

echo "Services starting... waiting 15 seconds for startup..."
sleep 15

# Check service status
echo "Checking service status..."
docker-compose -f docker-compose_ssl.yml ps

# Health checks
echo ""
echo "Performing health checks..."

# Check HTTP redirect
if curl -I -s http://$DOMAIN 2>/dev/null | grep -q "301"; then
    echo "✅ HTTP to HTTPS redirect working"
else
    echo "⚠️  Warning: HTTP redirect may not be working"
fi

# Check HTTPS
if curl -f -s https://$DOMAIN/api/v1/info > /dev/null 2>&1; then
    echo "✅ HTTPS API endpoint working"
else
    echo "❌ HTTPS API endpoint failed"
    echo "Checking logs..."
    docker-compose -f docker-compose_ssl.yml logs nginx
    exit 1
fi

echo ""
echo "🎉 CCDI API deployed successfully with SSL!"
echo ""
echo "🔒 Secure Access Points:"
echo "  HTTPS API: https://$DOMAIN"
echo "  API Info: https://$DOMAIN/api/v1/info"
echo "  Swagger Docs: https://$DOMAIN/docs"
echo "  API Endpoints: https://$DOMAIN/api/v1/{endpoint}"
echo ""
echo "� Management Commands:"
echo "  View logs: docker-compose -f docker-compose_ssl.yml logs -f"
echo "  Stop services: docker-compose -f docker-compose_ssl.yml down"
echo "  Restart: docker-compose -f docker-compose_ssl.yml restart"
echo ""
echo "📋 Certificate Info:"
echo "  Domain: $DOMAIN"
echo "  Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
echo "  Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
echo "  Auto-renewal: Managed by certbot container"
echo ""
echo "🌐 Test your API:"
echo "  curl https://$DOMAIN/api/v1/info"