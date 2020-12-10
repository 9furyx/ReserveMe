# ReserveMe
A reservation system for devices maintenance 
(This is a learning project of front-end and back-end)

## Deployment
Deploy this project wtih Docker Compose

1. Modify database password variable `POSTGRES_PASSWORD` in `db.env`

2. Modify jwt variable`SECRET_KEY` and `SECRET_KEY_REFRESH` in `server/.env`

3. Change `example.com` in `client/Caddyfile` and `client/.env` to your domain name

4. In the main directory, run

```
sudo docker-compose up -d
```

## Admin login
The defalut admin account is

Email: admin@example.com

Password: admin_password

You should change admin password after you login