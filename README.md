# Сервер Flask для приёма webhook's и пересылки их на target server

### Установка сервера

```
apt update

apt install nginx python3 python3-pip python3.12-venv certbot python3-certbot-nginx -y

cd /opt

git clone https://github.com/DrVidjet/in_webhook_flask.git

cd in_webhook_flask

cp API.conf.example API.conf
```

Прописываем target_url для пересылки

```
python3 -m venv .venv

source .venv/bin/acrivate

pip install -r requirements.txt

python3 proxy_server.py
```

### Настройка сервиса

```
sudo adduser --system --group in_webhook_flask_user --home /opt/in_webhook_flask

sudo chown -R in_webhook_flask_user:in_webhook_flask_user /opt/in_webhook_flask

nano /etc/systemd/system/in_webhook_flask.service
```

```
[Unit]
Description=Proxy Webhooks Flask
After=network.target

[Service]
WorkingDirectory=/opt/in_webhook_flask
ExecStart=/usr/bin/python3 /opt/in_webhook_flask/proxy_server.py
Restart=always
User=in_webhook_flask_user

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload

sudo systemctl enable --now in_webhook_flask

sudo systemctl status in_webhook_flask

git config --global --add safe.directory /opt/in_webhook_flask
```

### Настройка обратного прокси в примере nginx


`nano /etc/nginx/sites-available/in_webhook_flask`

```
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    server_name example.com;

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    location /webhook {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        return 404;
    }
}
```

### Получение ssl

```
dig example.com

certbot --nginx -d example.com

certbot renew --dry-run
```
