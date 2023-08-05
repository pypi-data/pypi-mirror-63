# Prophetable

    Define and run Prophet forecasting models using a configuration file.

`Prophet` is a python library from Facebook for forecasting time series data. Using `Prophetable`,
you can define a forecasting model by specifying parameters in a configurations file (`json`) or a
config object (`dict`).

## Configuring a model

Example data and configuration files include in the `data` directory of this project.

A minimal configuration looks like this:

```json

```

## Using the `Python` package

```sh
pip install prophetable
```

```python
from prophetable import Prophetable

p = Prophetable(config='/data/config.full.json')
p.run()
```

## Using Docker

```sh
```

### Cleanup Docker

```sh
docker stop pm
docker rm pm
```

## TODO

- Add advanced config for seasonalities that depend on other factors.
- Add advanced config for additional regressors.
