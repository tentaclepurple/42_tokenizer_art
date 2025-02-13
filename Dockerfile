FROM node:18

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install --save-dev hardhat
RUN npm install --save-dev dotenv
RUN npm install @nomiclabs/hardhat-ethers ethers dotenv
RUN npm install @nomiclabs/hardhat-waffle waffle chai
RUN npm install @openzeppelin/contracts@4.9.3

COPY . .

CMD [ "bash" ]