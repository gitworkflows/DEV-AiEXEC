# Running AiExec with Docker

This guide will help you get AiExec up and running using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Steps

1. Clone the AiExec repository:

   ```sh
   git clone https://github.com/khulnasoft-lab/aiexec.git
   ```

2. Navigate to the `docker_example` directory:

   ```sh
   cd aiexec/docker_example
   ```

3. Run the Docker Compose file:

   ```sh
   docker compose up
   ```

AiExec will now be accessible at [http://localhost:7860/](http://localhost:7860/).

## Docker Compose Configuration

The Docker Compose configuration spins up two services: `aiexec` and `postgres`.

### AiExec Service

The `aiexec` service uses the `khulnasoft/aiexec:latest` Docker image and exposes port 7860. It depends on the `postgres` service.

Environment variables:

- `AIEXEC_DATABASE_URL`: The connection string for the PostgreSQL database.
- `AIEXEC_CONFIG_DIR`: The directory where AiExec stores logs, file storage, monitor data, and secret keys.

Volumes:

- `aiexec-data`: This volume is mapped to `/app/aiexec` in the container.

### PostgreSQL Service

The `postgres` service uses the `postgres:16` Docker image and exposes port 5432.

Environment variables:

- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_DB`: The name of the PostgreSQL database.

Volumes:

- `aiexec-postgres`: This volume is mapped to `/var/lib/postgresql/data` in the container.

## Switching to a Specific AiExec Version

If you want to use a specific version of AiExec, you can modify the `image` field under the `aiexec` service in the Docker Compose file. For example, to use version 1.0-alpha, change `khulnasoft/aiexec:latest` to `khulnasoft/aiexec:1.0-alpha`.
