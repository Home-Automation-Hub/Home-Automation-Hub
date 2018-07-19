build:
	docker build -t home-automation-hub .

run: build
	docker-compose up -d --timeout=1
	docker ps

stop:
	docker-compose down --timeout=1