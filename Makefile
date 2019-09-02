run_dev: stop_dev
	docker-compose -f ./docker/docker-compose.yml up --build

stop_dev:
	docker-compose -f ./docker/docker-compose.yml down
