build:
	docker build -t home-automation-hub .

run: build
	docker-compose up -d
	docker ps

stop:
	docker-compose down