# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker Compose setup for running n8n locally with PostgreSQL database and public webhook access via ngrok tunnels. The repository provides a complete development environment with persistent data storage and database connectivity for n8n workflows.

The project includes a complete ticket/receipt processing workflow in the `ticket-reader/` folder with OCR capabilities and PostgreSQL integration.

## Architecture Components

- **n8n Service**: Workflow automation tool with PostgreSQL backend
- **PostgreSQL Service**: Database with pgvector extension for storing workflows, executions, and vector data
- **Docker Volumes**: Persistent storage for both n8n data and PostgreSQL data
- **ngrok Tunnel**: Public URL exposure for webhook integrations
- **Environment Configuration**: Centralized configuration via .env file

## Essential Commands

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your ngrok URL
WEBHOOK_URL=https://your-ngrok-url.ngrok.io
```

### Docker Compose Operations
```bash
# Start services (n8n + PostgreSQL)
docker compose up -d

# View service status
docker compose ps

# View logs
docker compose logs -f n8n
docker compose logs -f postgres

# Stop services
docker compose down

# Stop and remove volumes (destroys all data)
docker compose down -v
```

### Database Operations
```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U n8n -d n8n

# Create database backup
docker compose exec postgres pg_dump -U n8n n8n > backup.sql
```

### Tunnel Setup
```bash
# Configure ngrok with auth token
ngrok config add-authtoken YOUR_TOKEN_HERE

# Start tunnel for n8n
ngrok http 5678
```

### Access Points
- **Local n8n interface**: http://localhost:5678 (admin/admin123)
- **External webhook access**: https://your-ngrok-url.ngrok.io
- **PostgreSQL**: localhost:5432 (n8n/n8n_password)
- **Webhook endpoints**: https://your-ngrok-url.ngrok.io/webhook/webhook-id

## Development Workflow

1. **Environment Setup**: Copy .env.example to .env and configure variables
2. **Tunnel Setup**: Start ngrok tunnel and update WEBHOOK_URL in .env
3. **Launch Services**: Run docker compose up -d to start n8n and PostgreSQL
4. **Configure Workflows**: Access n8n interface and create workflows with database nodes
5. **Test Webhooks**: External services can send webhooks to the ngrok URL

## Important Notes

- This setup is for **development and testing only**, not production use
- Always update .env file with new ngrok URL when tunnel restarts
- The ngrok URL changes each time ngrok restarts (unless using paid ngrok account)
- PostgreSQL data persists between container restarts via Docker volumes
- n8n has basic authentication enabled (admin/admin123) for security