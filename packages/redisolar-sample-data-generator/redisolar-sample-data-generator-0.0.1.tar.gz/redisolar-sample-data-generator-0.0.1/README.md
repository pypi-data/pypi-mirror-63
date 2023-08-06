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

### Environment variables

Installing this package should add the "load_redisolar" command
to your path.

Before running this command, make sure to set the following required
environment variables, or you will get an error:

* REDISOLAR_REDIS_HOST - the hostname of your redis server
* REDISOLAR_REDIS_PORT - the port number of your redis server

Set either of the following optional environment variables:

* REDISOLAR_REDIS_PASSWORD - the password to your redis server
* REDISOLAR_REDIS_KEY_PREFIX - the prefix that you want to use for reidsolar keys (defaults to "app")

## Command

Run the `load_redisolar` command to generate sample data and persist
it in the target redis instance:

    load_redisolar
