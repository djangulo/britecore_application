# Denis Angulo's britecore application project

Hello, and welcome to my application project.

This project was built with the following technologies:

* django
* django-rest-framework
* Vue.js
* aws-cli
* pipenv

## Before installing

There are several steps to take prior to installation:

#### Configure aws-cli

Create a dir in ~/.aws/credentials with the following structure:

    [default]
    aws_access_key_id=YOURACCESSKEY
    aws_secret_access_key=YOURSECRETKEY

in order to not have to enter them for every call to aws-cli. You will also need to update 
`deploy/zappa_settings_template` "vpc_config, to contain your own `SubnetIds` and `SecurityGroupIds`


This project requires pipenv to deploy, so please install pipenv. Quoting the official docs:

If you're on MacOS, you can install Pipenv easily with Homebrew:

    $ brew install pipenv

Or, if you're using Fedora 28:

    $ sudo dnf install pipenv

You could otherwise install it directly with pip

    $ pip install --user pipenv

If all else fails, you could do a direct download:

    $ curl https://raw.githubusercontent.com/kennethreitz/pipenv/master/get-pipenv.py | python

Keep in mind that some distributions alias python 2 as python, and python3 for python 3.


## Deploy to AWS-Lambda

Once pipenv is installed, is as simple as running the script at `deploy/zappa_deploy.sh`.
**Prior** to running the script, you need to set the environment variables SQL_PASSWORD
and SECRET_KEY, the following snippets should do it

    $ export SQL_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')
    $ export SECRET_KEY=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')

Then the script will:

* run pipenv install
* create an AWS db-instance through the cli
* ping the database (through aws rds describe-db-instances) to check if the endpoint is       available
* when ready, it will proceed to deploy with zappa
* once deployed, it will migrate and create some sample risk policies to display

## Deploy with docker

Requirements:

* docker >= 18.09
* docker-compose >= 1.23.1
* docker-machine >= 0.16.0

Same as before, setup `~/.aws/credentials` appropriately. Then run

    $ docker-machine --driver amazonec2 --amazonec2-open-port 8000 --amazonec2-region us-east-2 britecore-app

Connect the machine as the active host:

    $ eval $(docker-machine env britecore-app)

