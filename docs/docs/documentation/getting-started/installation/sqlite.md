# Installing with SQLite

SQLite is a popular, open source, self-contained, zero-configuration database that is the ideal choice for Cena when you have 1-20 Users. Below is a ready to use docker-compose.yaml file for deploying Cena on your server.

**For Environmental Variable Configuration See:**

- [Frontend Configuration](/cena/documentation/getting-started/installation/frontend-config/)
- [Backend Configuration](/cena/documentation/getting-started/installation/backend-config/)

```yaml
---
version: "3.7"
services:
  cena-frontend:
    image: hkotel/cena:frontend-nightly
    container_name: cena-frontend
    environment:
    # Set Frontend ENV Variables Here
      - API_URL=http://cena-api:9000 # (1)
    restart: always
    ports:
      - "9925:3000" # (2)
    volumes:
      - cena-data:/app/data/ # (3)
  cena-api:
    image: hkotel/cena:api-nightly
    container_name: cena-api
    volumes:
      - cena-data:/app/data/
    environment:
    # Set Backend ENV Variables Here
      - ALLOW_SIGNUP=true
      - PUID=1000
      - PGID=1000
      - TZ=America/Anchorage
      - MAX_WORKERS=1
      - WEB_CONCURRENCY=1
      - BASE_URL=https://cena.yourdomain.com
    restart: always

volumes:
  cena-data:
    driver: local
```

<!-- Updating This? Be Sure to also update the Postgres Annotations -->

1. Whoa whoa whoa, what is this nonsense? The API_URL is the URL the frontend container uses to proxy api requests to the backend server. In this example, the name `cena-api` resolves to the `cena-api` container which runs the API server on port 9000. This allows you to access the API without exposing an additional port on the host.
    <br/> <br/> **Note** that both containers must be on the same docker-network for this to work.
2.  To access the cena interface you only need to expose port 3000 on the cena-frontend container. Here we expose port 9925 on the host, feel free to change this to any port you like.
3.  Mounting the data directory to the frontend is now required to access the images/assets directory. This can be mounted read-only. Internally the frontend containers runs a Caddy proxy server that serves the assets requested to reduce load on the backend API.
