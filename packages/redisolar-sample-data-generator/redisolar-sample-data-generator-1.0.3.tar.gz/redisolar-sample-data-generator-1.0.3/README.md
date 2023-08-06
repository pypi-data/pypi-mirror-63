# Redisolar Sample Data Generator

This is a fast sample data generator for the Education team's
"redisolar" applications.


## Python Version

This package requires Python 3.7.


## Installation

After checking out the repository, make sure you are using a virtualenv.
Create one in the checkout directory like this:

    python3 -m venv env


Then activate it:

    source env/bin/activate

Next you can install the Python dependencies with pip:
    
    pip install .

If you're going to work on the code, install it in "editable" mode
and include the dev dependencies:

    pip install -e ".[dev]"

## Running

This package installs the `load_redisolar` command. Running it generates
sample data and uploads it to a target Redis instance.

By default, `redisolar` uploads to a Redis instance running on localhost at
port 6379, with no password. It uses an included JSON fixture file containing
Site data.

You can override the hostname, port, and fixture file with the `--hostname`,
`--port`, and `--filename` options:

    $ load_redisolar --hostname 192.168.1.2 --port 16379 --filename path/to/sites.json

### Specifying a password

For password-protected Redis instances, you can specify a password
interactively with the `--request-password` option.

    $ load_redisolar --request-password
    Redis password: xyz

Specify a password non-interactively by setting the environment variable
`REDISOLAR_REDIS_PASSWORD`.

    $ export REDISOLAR_REDIS_PASSWORD=xyz
    $ load_redisolar
