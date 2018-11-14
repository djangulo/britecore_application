FROM node:10.11.0-alpine
WORKDIR /usr/src/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

