# networking_data_generation

Tools for generating network graphs, computing structural reliability functions, and simulating node failures.

## Components

- **NetworkProcessing** — graph generation (via igraph), min-path/min-cut structural functions, and failure simulation (exponential/Weibull).
- **NetworkProcessingDbLogic** — async PostgreSQL persistence for graphs (SQLAlchemy).
- **NetworkProcessingWebApp** — aiohttp API served with gunicorn.

## Run with Docker

```bash
docker compose up --build
```

The web app is available at http://localhost:8080. PostgreSQL runs on port 5432 (`networks` database, user `postgres`, password `test`).

Initialize the schema:

```bash
psql -h localhost -U postgres -d networks -f create_tables.sql
```

## Project layout

```
NetworkProcessing/          # Core graph and reliability logic
NetworkProcessingDbLogic/   # Database models and controller
NetworkProcessingWebApp/    # Web application
create_tables.sql           # PostgreSQL schema
docker-compose.yaml         # Local dev stack
```
