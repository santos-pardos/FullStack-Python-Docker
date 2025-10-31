# Despliegue multi‑contenedor con Docker Compose (FinTech Solutions)

## Estructura
```
.
├─ docker-compose.yml
├─ .env
├─ reverse-proxy/
│  └─ nginx.conf
├─ api/
│  ├─ Dockerfile
│  ├─ app.py
│  └─ requirements.txt
├─ web/
│  ├─ Dockerfile
│  └─ build/index.html
├─ db/
│  └─ init/init.sql
└─ Makefile
```

## Ejecución
1. Crear `.env` (ya incluido) y ajustar puertos si hace falta.
2. Levantar todo: `make up` o `docker compose --env-file .env up -d --build`
3. Verificar salud:
   - `docker compose ps`
   - `curl http://localhost:${PROXY_HTTP_PORT}/health`
   - `curl http://localhost:${API_PORT}/health`
4. Probar en navegador:
   - Web: `http://localhost:${PROXY_HTTP_PORT}`
   - Adminer: `http://localhost:${ADMINER_PORT}` (host `db`, puerto `5432`, user `${POSTGRES_USER}`)
5. Logs: `docker compose logs -f api`

## Comprobaciones
- `docker compose ps` con estados `healthy`.
- Navegador sirviendo la web y la API vía proxy (`/api/...`).
- Adminer conectado y tablas visibles.
- `docker volume ls` (volumen `pgdata`).
- `docker network ls` y `docker inspect` (resumen).

## DBeaver
```
docker run --network fullstack-python-docker_backnet --name cloudbeaver --rm -ti -d -p 8978:8978 -v /opt/cloudbeaver/workspace dbeaver/cloudbeaver:latest
```

## Notas
- La API usa `DATABASE_URL` -> `postgresql://fintech:fintechpassword@db:5432/fintechdb`.
- `reverse-proxy` enruta `/` a `web` y `/api/` a `api`.

## Tool
```
docker run -it  --network fullstack-python-docker_backnet nicolaka/netshoot sh
```

## Install Docker and Docker-Compose - Ubuntu
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo apt install docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
docker-compose --version
```

```
sudo usermod -aG docker $USER
(salir y entrar de ssh)
sudo apt install git -y
sudo apt install unzip -y
```

