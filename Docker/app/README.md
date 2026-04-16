# Docker Learning App

This is a small Python + Flask app meant for learning:

- `Dockerfile`
- `docker build`
- `docker run`
- `docker compose`
- environment variables
- port mapping
- bind mounts

## Files

- `app.py`: simple Flask app
- `requirements.txt`: Python dependencies
- `Dockerfile`: image definition
- `docker-compose.yml`: local multi-container style workflow, even though this example uses one service

## Run without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: <http://localhost:8000>

## Build the image

```bash
docker build -t docker-learning-app .
```

## Run the container

```bash
docker run --rm -p 8000:8000 docker-learning-app
```

Try passing environment variables:

```bash
docker run --rm -p 8000:8000 \
  -e APP_ENV=production \
  -e APP_MESSAGE="Hello from docker run" \
  docker-learning-app
```

## Run with Docker Compose

```bash
docker compose up --build
```

Because the compose file mounts the current folder into `/app`, code changes on your machine are reflected inside the container. That makes it useful for learning and local development.

## Useful experiments

1. Change `APP_MESSAGE` in `docker-compose.yml` and run `docker compose up --build`.
2. Change the exposed port mapping from `8000:8000` to `9000:8000`.
3. Remove the `volumes` section and see how container behavior changes.
4. Add another route in `app.py`, then rebuild and rerun.
5. Run `docker ps`, `docker images`, and `docker logs <container-id>`.
