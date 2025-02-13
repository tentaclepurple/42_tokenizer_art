all:
	docker compose up -d

down:
	docker compose down

exec:
	docker exec -it nft42-hardhat bash

compile:
	npx hardhat compile

deploy:
	npx hardhat run deployment/deploy.js --network amoy


mint:
	npx hardhat run mint/mint.js --network amoy

verify:
	npx hardhat run deployment/verify.js --network amoy

id:
	npx hardhat run deployment/getTokenId.js --network amoy

geturis:
	npx hardhat run deployment/getTokenURIs.js --network amoy

clean: down
	docker system prune -a -f

.PHONY: verify mint deploy compile exec down all clean