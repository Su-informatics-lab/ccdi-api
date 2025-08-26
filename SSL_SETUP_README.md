# CCDI API SSL Setup Guide

## SSL Configuration for ccdi.ipo.sulab.io

This guide provides step-by-step instructions to scurl -I http://ccdi.ipo.sulab.io

# Test HTTPS redirect
curl -I https://ccdi.ipo.sulab.io

# Test API endpoint
curl https://ccdi.ipo.sulab.io/api/v1/infoSL/TLS encryption for the CCDI API using Let's Encrypt certificates.

### Prerequisites

1. **Domain**: (configured and pointing to your server)
2. **Email**: (for Let's Encrypt notifications)
3. **Certbot**: Already installed on Ubuntu server
4. **Docker**: Docker and Docker Compose installed
5. **Ports**: 80 and 443 open in firewall

### Files Created

- `nginx_ssl.conf` - SSL-enabled nginx configuration
- `docker-compose_ssl.yml` - Docker Compose with SSL support
- `setup_ssl.sh` - Script to obtain SSL certificates
- `deploy-production_ssl.sh` - Script to deploy with SSL

### Setup Process

#### Step 1: Obtain SSL Certificate

On your Ubuntu server, run the SSL setup script:

```bash
./setup_ssl.sh
```

This will:
- Create required directories
- Stop existing containers
- Start temporary nginx for ACME challenge
- Obtain SSL certificate from Let's Encrypt
- Generate DH parameters for security
- Clean up temporary files

#### Step 2: Deploy with SSL

After obtaining certificates, deploy the API with SSL:

```bash
./deploy-production_ssl.sh
```

This will:
- Verify certificates exist
- Stop existing containers
- Start services with SSL configuration
- Perform health checks
- Display access information

### SSL Configuration Details

#### Security Features

- **TLS 1.2 and 1.3** support
- **Strong cipher suites** for encryption
- **HSTS headers** (HTTP Strict Transport Security)
- **Security headers** (X-Frame-Options, CSP, etc.)
- **DH parameters** for perfect forward secrecy
- **Automatic HTTP to HTTPS redirect**

#### Certificate Management

- **Auto-renewal**: Certbot container runs every 12 hours
- **Location**: `/etc/letsencrypt/live/ccdi.ipo.sulab.io/`
- **Files**:
  - `fullchain.pem` - Certificate chain
  - `privkey.pem` - Private key
  - `ssl-dhparams.pem` - DH parameters

### Access Points (After SSL Setup)

- **HTTPS API**: https://ccdi.ipo.sulab.io
- **API Info**: https://ccdi.ipo.sulab.io/api/v1/info
- **Swagger Docs**: https://ccdi.ipo.sulab.io/docs
- **All Endpoints**: https://ccdi.ipo.sulab.io/api/v1/{endpoint}

### Management Commands

```bash
# View logs
docker-compose -f docker-compose_ssl.yml logs -f

# Stop services
docker-compose -f docker-compose_ssl.yml down

# Restart services
docker-compose -f docker-compose_ssl.yml restart

# Check certificate status
sudo certbot certificates

# Manual certificate renewal (if needed)
sudo certbot renew

# Check service status
docker-compose -f docker-compose_ssl.yml ps
```

### Troubleshooting

#### Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Test certificate renewal
sudo certbot renew --dry-run

# View nginx logs
docker-compose -f docker-compose_ssl.yml logs nginx
```

#### Connection Issues

```bash
# Test HTTP redirect
curl -I http://ccdi.ipo.sulab.io

# Test HTTPS connection
curl -I https://ccdi.ipo.sulab.io

# Test API endpoint
curl https://ccdi.ipo.sulab.io/api/v1/info
```

#### Port Issues

```bash
# Check if ports are open
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Check firewall (if using ufw)
sudo ufw status
```

### Certificate Renewal

The certbot container automatically renews certificates. For manual setup, add to crontab:

```bash
# Edit crontab
sudo crontab -e

# Add these lines for twice-daily renewal checks
0 12 * * * /usr/bin/certbot renew --quiet
0 0 * * * /usr/bin/certbot renew --quiet
```

### Security Best Practices

1. **Regular Updates**: Keep Docker images updated
2. **Monitoring**: Monitor certificate expiration
3. **Backups**: Backup `/etc/letsencrypt` directory
4. **Firewall**: Only open required ports (80, 443)
5. **Logs**: Monitor nginx and application logs

### Quick Test

After deployment, test the API:

```bash
# Test HTTPS endpoint
curl https://ccdi.ipo.sulab.io/api/v1/info

# Test SSL certificate
openssl s_client -connect ccdi.ipo.sulab.io:443 -servername ccdi.ipo.sulab.io < /dev/null
```

### Support

For issues:
1. Check logs: `docker-compose -f docker-compose_ssl.yml logs`
2. Verify domain DNS resolution
3. Check firewall settings
4. Ensure certbot is working: `sudo certbot --version`
