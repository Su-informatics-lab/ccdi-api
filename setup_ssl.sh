#!/bin/bash

# SSL Setup Script for CCDI API
# Domain: ccdi.cis230185.projects.jetstream-cloud.org
# Email: wang208@iu.edu

set -e

DOMAIN="ccdi.cis230185.projects.jetstream-cloud.org"
EMAIL="wang208@iu.edu"

echo "🔐 Setting up SSL certificates for $DOMAIN..."

# Create required directories
sudo mkdir -p /var/www/certbot
sudo mkdir -p /etc/letsencrypt

# Stop any running containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose_ssl.yml down 2>/dev/null || true

# Create temporary nginx config for certificate acquisition
echo "Creating temporary nginx configuration..."
cat > nginx-temp.conf << EOF
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name $DOMAIN;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 200 'CCDI API - Obtaining SSL Certificate...';
            add_header Content-Type text/plain;
        }
    }
}
EOF

# Start temporary nginx container for ACME challenge
echo "Starting temporary nginx for ACME challenge..."
docker run -d --name temp-nginx \
    -p 80:80 \
    -v $(pwd)/nginx-temp.conf:/etc/nginx/nginx.conf:ro \
    -v /var/www/certbot:/var/www/certbot:ro \
    nginx:alpine

sleep 5

echo "Obtaining SSL certificate for $DOMAIN..."

# Get certificate using certbot
sudo certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d $DOMAIN

# Stop temporary nginx
echo "Cleaning up temporary nginx..."
docker stop temp-nginx 2>/dev/null || true
docker rm temp-nginx 2>/dev/null || true

# Generate DH parameters if they don't exist
if [ ! -f "/etc/letsencrypt/ssl-dhparams.pem" ]; then
    echo "Generating DH parameters..."
    sudo openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048
fi

# Clean up temporary files
rm -f nginx-temp.conf

echo "✅ SSL certificate obtained successfully!"
echo ""
echo "Certificate files created:"
echo "  - Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
echo "  - Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
echo "  - DH Params: /etc/letsencrypt/ssl-dhparams.pem"
echo ""
echo "🚀 Ready to deploy with SSL!"
echo "Run: ./deploy-production_ssl.sh"