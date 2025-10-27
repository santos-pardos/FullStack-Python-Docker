up:
	docker compose --env-file .env up -d --build

logs:
	docker compose logs -f

down:
	docker compose down

clean:
	docker compose down -v
	docker system prune -f
