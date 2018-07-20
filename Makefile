build:
	docker build -t home-automation-hub .

run: build
	docker-compose up -d --timeout=1
	docker ps

run-interactive: build
	docker-compose up --timeout=1

stop:
	docker-compose down --timeout=1