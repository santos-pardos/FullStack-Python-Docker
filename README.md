# Act 2 – Despliegue multi‑contenedor con Docker Compose (FinTech Solutions)

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

## Notas
- La API usa `DATABASE_URL` -> `postgresql://fintech:fintechpassword@db:5432/fintechdb`.
- `reverse-proxy` enruta `/` a `web` y `/api/` a `api`.
