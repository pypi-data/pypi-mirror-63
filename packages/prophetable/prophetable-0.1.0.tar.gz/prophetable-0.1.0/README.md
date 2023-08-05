# Prophetable

Run fbprophet from config files. Runnable from docker.

## Quick start

```sh
docker build -t prophetable . && \
docker run --rm -d \
    -v /full/path/to/volume:/data \
    --name=pm \
    prophetable
```

## Build

```sh
docker build -t prophetmodeller .

# Clean rebuild
# docker build --no-cache -t prophetmodeller .
```

## Run

```sh
docker run --rm -d \
    -v /full/path/to/volume:/data \
    --name=pm \
    prophetable
```

## Log

```sh
docker logs pm
```

## Stop

```sh
docker stop pm
```

## Cleanup

```sh
docker rm pm
```

## TODO

- Publish as package to use separately from docker
- Seasonalities that depend on other factors
- Additional regressors
