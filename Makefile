run:
	docker-compose up -d
	docker ps

backend-dependencies:
	cd src; pip

frontend-dependencies:
	cd src; yarn install

frontend: frontend-dependencies
	cd src;	yarn run build:dev

stop:
	docker-compose down