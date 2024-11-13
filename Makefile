.PHONY: run-kafka
run-kafka:
	@docker-compose up -d kafka kafka-web

.PHONY: run-database
run-database:
	@docker-compose up -d postgres-env pgadmin

.PHONY:
run-elastic:
	@docker-compose up -d elasticsearch kibana

.PHONY:
stop-elastic:
	@docker-compose down elasticsearch kibana

.PHONY:
purge-elastic:
	@docker-compose down -v elasticsearch kibana

.PHONY: run-pipeline-apps
run-pipeline-kb-apps:
	@docker-compose up -d parser 
	@docker-compose up -d classifier 
	@docker-compose up -d db_sync --remove-orphans

.PHONY: produce-example-message
produce-example-message:
	@docker-compose up initial-payload-producer

stop-all:
	@docker-compose down

run-unit-tests:
	@docker-compose run --rm --remove-orphans parser poetry run pytest tests/unit-tests/test_parser.py
	@docker-compose run --rm --remove-orphans classifier poetry run pytest tests/unit-tests/test_identifier.py
	@docker-compose run --rm --remove-orphans indexer poetry run pytest -s  tests/unit-tests/test_index_utils.py
	@docker-compose run --rm --remove-orphans searcher poetry run pytest -s  tests/unit-tests/test_searcher_utils.py

.PHONY: 
run-integration-topics-tests:
	@docker-compose run --rm --remove-orphans parser poetry run pytest tests/integration-tests/test_parser_integration.py
	@docker-compose run --rm --remove-orphans classifier poetry run pytest tests/integration-tests/test_classifier_integration.py
	@docker-compose run --rm --remove-orphans db_sync poetry run pytest tests/test_db_sync_integration.py

.PHONY: 
run-integration-search-tests:
	@docker-compose run --rm --remove-orphans indexer poetry run pytest -s  tests/integration-tests/test_index_integration.py

.PHONY: run-integration-tests
run-integration-tests: run-integration-topics-tests run-integration-search-tests

.PHONY: run-coletas-api
run-coletas-api:
	@docker-compose up -d mongodb
	@docker-compose up -d coletasapi
	@docker-compose up -d tests

run-send-requests-to-coletasapi:
	@docker-compose run --rm --remove-orphans indexer poetry run python3 populate-by-collector/populate.py

run-indexer-pipeline:
	@docker-compose run --rm --remove-orphans indexer poetry run python3 main.py 

run-searcher:
	@docker-compose up -d searcher 

run-graphql:
	@docker-compose up -d backend

run-frontend:
	@docker-compose up -d frontend

run-mock-api:
	@docker-compose up -d mock-api

.PHONY: run-infra
run-app: run-kafka run-database run-elastic run-pipeline-kb-apps run-coletas-api run-searcher run-mock-api run-graphql run-frontend