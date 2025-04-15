NAME=datascience_pg

all: up

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker stop postgres_data pgadmin_data 2>/dev/null || true
	docker rm -f postgres_data pgadmin_data 2>/dev/null || true

fclean: clean
	docker volume rm postgres_data pgadmin_data 2>/dev/null || true
	docker network prune -f --force

re: fclean up