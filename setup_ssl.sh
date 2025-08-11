#!/bin/bash

# SSL Setup Script for CCDI API
set -e

DOMAIN="your-domain.com"
EMAIL="your-email@example.com"

echo "Setting up SSL certificates for $DOMAIN..."

# Create required directories
sudo mkdir -p /var/www/certbot
sudo mkdir -p /etc/letsencrypt

# Stop any running containers
docker-compose down

# Start nginx without SSL first (for initial certificate generation)
cat > nginx-temp.conf << EOF
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name $DOMAIN www.$DOMAIN;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 200 'OK';
            add_header Content-Type text/plain;
        }
    }
}
EOF

# Start temporary nginx
docker run -d --name temp-nginx \
    -p 80:80 \
    -v $(pwd)/nginx-temp.conf:/etc/nginx/nginx.conf:ro \
    -v /var/www/certbot:/var/www/certbot:ro \
    nginx:alpine

echo "Obtaining SSL certificate..."

# Get certificate
sudo certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

# Stop temporary nginx
docker stop temp-nginx
docker rm temp-nginx

# Generate DH parameters
sudo openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048

# Clean up
rm nginx-temp.conf

echo "SSL certificate obtained successfully!"
echo "Now update nginx.conf with your domain name and start the services:"
echo "1. Replace 'your-domain.com' in nginx.conf with '$DOMAIN'"
echo "2. Run: docker-compose --profile ssl up -d"