# Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Build backend + setup nginx
FROM python:3.11-slim

# Install nginx and curl for healthcheck
RUN apt-get update && apt-get install -y nginx curl supervisor && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend to nginx
COPY --from=frontend-builder /app/dist /usr/share/nginx/html

# Configure nginx
RUN rm -f /etc/nginx/sites-enabled/default && cat > /etc/nginx/sites-available/default << 'EOF'
server {
    listen 8080 default_server;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Configure supervisor to run both services
RUN cat > /etc/supervisor/conf.d/services.conf << 'EOF'
[supervisord]
nodaemon=true

[program:uvicorn]
directory=/app/backend
command=uvicorn main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
stderr_logfile=/var/log/uvicorn.err.log
stdout_logfile=/var/log/uvicorn.out.log

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stderr_logfile=/var/log/nginx.err.log
stdout_logfile=/var/log/nginx.out.log
EOF

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/services.conf"]
