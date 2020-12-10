FROM node:latest as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY ./ .

RUN npm run build

FROM caddy as production-stage

COPY Caddyfile /etc/caddy/Caddyfile

COPY --from=build-stage /app/dist /srv