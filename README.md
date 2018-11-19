# Denis Angulo's BriteCore project submission

## TOC<a name="toc"></a>

- [About](#about)
- [Links to deployed versions](#links)
    - [AWS Lambda](#aws-lambda)
    - [AWS EC2 (with docker)](#aws-ec2)
- [Approach](#approach)
- [Deliverable summary](#deliverables)
- [Deployment](#deployment)
    - [Before deploying](#before-deploying)
        - [Configuring AWS cli](#configure-aws-cli)
        - [Pipenv](#configure-pipenv)
        - [Additional deployment notes](#addtl-deployment-notes)
    - [Deploy to AWS-Lambda](#deploy-aws-lambda)
    - [Deploy to AWS-EC2](#deploy-aws-ec2)
    - [Un-deploy](#undeploy)
- [Closing comments](#closing-comments)

## About<a name="about"></a>

Hello, and welcome to my application project.

This is Denis Angulo's project submission for the Software Developer (Product Development) postion (posted [here](https://engineering-application.britecore.com/do/product-engineer-western-hemisphere)).

This project was built with the following technologies:

* django
* django-rest-framework
* Vue.js
* Amazon Web Services
* aws-cli
* Docker
* pipenv
* Bootstrap4

## Links to the deployed version<a name="links"></a>

#### AWS-Lambda<a name="aws-lambda"></a>

Main page:

https://bkw3yst1yb.execute-api.us-east-2.amazonaws.com/prod

API root view:

https://bkw3yst1yb.execute-api.us-east-2.amazonaws.com/prod/api/v1.0/


#### AWS EC2<a name="aws-ec2"></a>

Main page:

http://18.191.189.208

API root view:

http://18.191.189.208/api/v1.0/


[Back to TOC](#toc)

---

## My approach<a name="approach"></a>

The way this solution would allow clients to define their own models, is by giving them the freedom to create fields as they would please. These fields, attached to a Risk description, would then trigger a new database table creation (not implemented).

In this way, the models presented in the `risks/models.py` file would act as metadata tables, holding the data that would allow the system to connect to the actual database tables.

Database table names would be defined by the insurer, as defined by the RiskType name.
The insurer would be able to attach as many FieldTypes(to the RiskType object), as they would like, naming without restrictions, as they will only pertain to a particular risk.

I decided to use Django with Django-REST-Framework, as it is an incredibly powerful tool for API creation.

The tables were modeled rather straightforwardly (by Django standards), by creating a RiskType model, and a FieldType model, then relating the FieldType to the RiskType via a foreign key. They're arranged as follows:

RiskType model has:

- A `name` field (CharField).
- A `description` field (CharField).

FieldType model has:

- `name` field (CharField).
- `data_type` field, IntegerField with choices.
- `help_text` field, CharField (seemed appropriate as these will emulate form fields).
- `number_of_fields`, convenience field for Enum types. I'm well aware this is not the best approach to having Enums with multiple form fields ([Postgres's Array Field](https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/#arrayfield) field using [Django's MultiWidget](https://docs.djangoproject.com/en/2.1/ref/forms/widgets/#django.forms.MultiWidget) would have been a better solution, in my opinion). Nevertheless, since I implemented all my forms with JavaScript (Vue.js, more precisely), MultiWidget was not an option. This approach seemed to offer the best benefits for the scope and time constraints of this project.
- `risk` field. Not-required, nullable foreign key field to the RiskType model.

You would notice that neither the RiskType or FieldType's names are unique, this was by design, since the frontend tightly couples the FieldType to the RiskType on creation. This prevents accidentally deleting some other RiskType's fields when deleting any RiskType instance.

I left the foreign key un-required (blank=True) and nullable, this way I'm allowed to hit the API to create FieldType objects without having to attach it to a RiskType object. I also added a `bulk_add_fields` convenience method to the RiskType model, to get-or-create an incoming FieldType set on the RiskType API endpoint.

For the frontend, I embedded a Vue.js instance into a TemplateView (instanced directly in `britecore_application/urls.py`). All API calls and form rendering through the Vue app.

The full implementation (what is implied by the description) is that this will be a dynamic model generator, where the Django API and models act as metadata tables, who in turn are pointed programmatically to another database containing the actual tables for the forms generated by Vue and the API.

I understand this is a concept project, but if I had to fully implement the description above, I would do so by creating an AWS DynamoDB instance (or any other NOSQL database), with endpoints that accept AJAX calls from our Vue instance. NOSQL offers more flexibility when it comes to dynamic models like this one (SQL schemas can be rather rigid, specially if scaled).

[Back to TOC](#toc)

---

## Deliverables<a name="deliverables"></a>

1. A README that describes your approach and how to deploy your project.
    - You're reading it!
    - For details about deployment, see the [deployment](#deployment) section.
2. Link(s) to the deployed version of your project.
    - See [links](#links)
3. Bonus points if you also orchestrate the launch environment in AWS using CloudFormation.
    - I did not see the need of orchestrating the creation of say, an EC2 instance when the AWS-lambda deployment is serverless. If you would accept it, I would like to offer the [docker deployment](#deploy-aws-ec2) instead.
4. Mega bonus points if you host the app in AWS Lambda using Zappa or AWS ECS using AWS Fargate.
    - See [the AWS-Lambda deployment section](#deploy-aws-lambda)
5. A Python file containing the ORM classes for these tables.
    - See `risks/models.py`
    - A copy of the `models.py` file is found in the `deliverables` directory.
6. An entity relationship diagram, which depicts the tables and their relationship to one another.
    - See below
    - A copy of the `ERD.png` file is found on the `deliverables` directory.
    <p align="center">
    <img src="deliverables/ERD.png" alt="Employee relationship diagram"/>
    </p>
7. A well-tested REST API written in Python.
    - Tests are found in `risks/tests/test_api.py`.
    - I have left Django-REST-framework's DefaultRouter explorer view enabled,
    in case you want to explore the API. You can find direct links in [the links section](#links)
8. If using Django, you must use Django and/or Django REST Framework's Class-Based Views.
    - See the `risks/api.py` file, where I used Django REST framework Viewsets.
9. Create a single page that hits your risk type API endpoint(s) and displays all of the fields to the user in 
a form. Be sure to display at least one field of each type on the page. Don't worry about submitting the 
form.
    - It's the main page of the application (see [links](#links). The column on the left allows you to:
        - Select one of the existing Risk Types
        - Create a new Risk Type
            - Click the "Add field" button to add fields
            - Then
                - Select the field type
                - Add a name for the field
                - Add help text for the field
                - (ENUM only) add the number of inputs to display
10. Fields should use appropriate widgets based on their type. text fields should display as text boxes, date 
fields should use date pickers, and so on.
    - Please click any of the sample Risk Types to see the field forms implemented.
11. Bonus points if you come up with an elegant response for when users click on an unactivated form submit 
button.
    - I'm afraid it's not as elegant as I'd like, just a disabled button.
12. Mega bonus points for handling form submission.
    - The actual risk information form submission is not handled, as the project is not fully implemented.
    - Form submission for risk creation *is* implemented.


[Back to TOC](#toc)

---

# Deployment<a name="deployment"></a>

## Before deploying<a name="before-deploying"></a>

There are several steps to take prior to installation:

#### Configure aws-cli<a name="configure-aws-cli"></a>

Create a dir in ~/.aws/credentials with the following structure:

    [default]
    aws_access_key_id=YOURACCESSKEY
    aws_secret_access_key=YOURSECRETKEY

in order to not have to enter them for every call to aws-cli. You will also need to update 
`deploy/zappa_settings_template` "vpc_config, to contain your own `SubnetIds` and `SecurityGroupIds`

#### Pipenv<a name="configure-pipenv"></a>

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

#### Additional deployment notes<a name="addtl-deployment-notes"></a>

Besides the dependencies above, the scripts make heavy use of [gnu sed](https://www.gnu.org/software/sed/) and [gnu grep](https://www.gnu.org/software/grep/). Remember that if any of the scripts fail to run, you can just run the commands manually to deploy.

[Back to TOC](#toc)

---

## Deploy to AWS-Lambda<a name="deploy-aws-lambda"></a>

Once pipenv is installed, is as simple as running the script at `deploy/zappa_deploy.sh`.

**Prior** to running the script, you need to set the environment variables SQL_PASSWORD
and SECRET_KEY, the following snippets should do it

    $ export SQL_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')
    $ export SECRET_KEY=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')

This deployment takes more time, as it needs to wait for the RDS Postgres instance to be available before proceeding to deploy the django app.

Then the script will:

* run pipenv install
* create an AWS db-instance through the cli
* ping the database (through `aws rds describe-db-instances`) to check if the endpoint is       available
* when ready, it will proceed to deploy with zappa
* once deployed, it will migrate and create some sample risk policies to display

[Back to TOC](#toc)

---

## Deploy to AWS EC2 with docker<a name="deploy-aws-ec2"></a>

Requirements:

* docker >= 18.09
* docker-compose >= 1.23.1
* docker-machine >= 0.16.0

Same as before, setup `~/.aws/credentials` appropriately. Then run `deploy/docker_deploy.sh`.

This script will do the following:

    $ docker-machine create --driver amazonec2 --amazonec2-open-port 80 --amazonec2-region us-east-2 britecore-app

Connect the machine as the active host:

    $ eval $(docker-machine env britecore-app)

Then run 

    $ docker-compose up --build -d

The instance will be running at the public IP of the docker-machine (you can check with `docker-machine ls`).

[Back to TOC](#toc)

---

## Un-deploy<a name="undeploy"></a>

To take down the app:

* If deployed with AWS/Zappa, run `pipenv run zappa undeploy -y`
* If you used Docker, run `docker-machine rm -y britecore-app`

[Back to TOC](#toc)

---


## Closing comments<a name="closing-comments"></a>

Thank you for taking the time to review my project.

I have thoroughly enjoyed working on this project. Even though I used technologies I'm very familiar with (Django, Django-REST-Framework), I had the chance to work with some other technologies that I did not have a lot of experience with (Vue, AWS); and some that are entirely new to me (Zappa is my new favorite toy!).

Once again, thank you for your time.

Kind regards,

\- Denis Angulo

[Back to TOC](#toc)

