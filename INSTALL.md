# Installing

GeoKrety API can be configured and launched in 2 different modes.

* Production
* Development

## Python dependencies

```
pip install -r requirements/prod.txt
```
```
pip install -r requirements/dev.txt
```

## Configure

Copy file `.env.example` to `.env` and edit as necessary. Take care to your database configuration.

**Please never commit `.env` file to the repository**

```
DATABASE_URL=mysql+mysqldb://geokrety:test@127.0.0.1/geokrety

TEST_DATABASE_URL=mysql+mysqldb://geokrety_unittest:test@127.0.0.1/geokrety_unittest

APP_CONFIG=config.DevelopmentConfig

SENTRY_DSN=https://3xxxxxx16fbc9:8xxxxxx81fb70@sentry.io/111111
```

`APP_CONFIG` can be of:
* ProductionConfig
* DevelopmentConfig

### Sentry

Application exceptions can be collected to sentry. Please create an account there and add the configuration to your `.env`.

```
SENTRY_DSN=https://<user>:<pass>@sentry.io/<number>
```

## Launch application

```
gunicorn -w 1 -b 0.0.0.0:5000 --reload app:app
```

# Running with Docker

Please see `docker-compose.yml`.
