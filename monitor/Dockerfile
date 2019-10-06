FROM node

WORKDIR /usr/src/app
COPY package.json package-lock.json /usr/src/app/

RUN npm install

COPY . /usr/src/app/
RUN npm run build