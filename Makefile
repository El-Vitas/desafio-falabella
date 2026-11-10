COMPOSE := docker compose
TEST_COMPOSE := docker compose -f docker-compose.test.yml
TEST_SUITES := extraction-tests pipeline-tests api-tests web-tests

.DEFAULT_GOAL := help
.PHONY: help up down reset data data-force dag test logs psql

help:
	@echo "make up          build and start everything (creates .env from .env.example if missing)"
	@echo "make data        run the extraction and the generator (skipped if data/_SUCCESS exists)"
	@echo "make data-force  download from PokeAPI again and regenerate the data"
	@echo "make dag         trigger the pokemon_pipeline DAG"
	@echo "make test        run every test suite in Docker"
	@echo "make logs        follow the logs of every service"
	@echo "make psql        open a SQL console on the pokemon database"
	@echo "make down        stop everything, keeping the database"
	@echo "make reset       stop everything and delete the database volume"

.env:
	cp .env.example .env

up: .env
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

reset:
	$(COMPOSE) down -v

data: .env
	$(COMPOSE) run --rm data-init

data-force: .env
	FORCE_EXTRACT=true $(COMPOSE) run --rm data-init

dag:
	$(COMPOSE) exec airflow airflow dags trigger pokemon_pipeline

test:
	@status=0; \
	for suite in $(TEST_SUITES); do \
		$(TEST_COMPOSE) run --rm $$suite || status=1; \
	done; \
	$(TEST_COMPOSE) down -v; \
	exit $$status

logs:
	$(COMPOSE) logs -f

psql:
	$(COMPOSE) exec postgres psql -U postgres -d pokemon
