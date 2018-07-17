build:
	docker build -t home-automation-hub .

run: build
	docker-compose up -d
	docker ps

# TODO: Move Yarn and Pip stuff into dockerfile
backend-dependencies:
	cd src; pip

frontend-dependencies:
	cd src; yarn install

frontend: frontend-dependencies
	cd src;	yarn run build:dev

stop:
	docker-compose down