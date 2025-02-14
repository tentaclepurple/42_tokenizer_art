FROM node:18

WORKDIR /app
COPY package*.json ./


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv


RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN npm install
RUN npm install --save-dev hardhat
RUN npm install --save-dev dotenv
RUN npm install @nomiclabs/hardhat-ethers ethers dotenv
RUN npm install @nomiclabs/hardhat-waffle waffle chai
RUN npm install @openzeppelin/contracts@4.9.3

RUN python3 -m venv venv
RUN echo 'alias py="python3"' >> /root/.bashrc
RUN echo 'source venv/bin/activate' >> /root/.bashrc
RUN echo 'pip install -r requirements.txt' >> /root/.bashrc


COPY . .

CMD [ "bash" ]