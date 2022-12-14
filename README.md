# Django microservice template
A template for creating Django microservices that include support for Docker, Kubernetes, CI/CD, data synchronization and more!

This repository contains a template that can be used or aid in the following situations:
- Building a system developed by multiple teams. Each responsible for their own microservice.
- Developing a complex system based on individual modules.
- Add resiliency in deployment, by only updating parts of a system and having lose connection between microservices.
- Automatic management of deployment and scaling.

Microservices allows use to tackle development of complex systems, and thus, there area a lot of concepts involved. Is not necessary to get deep in to this topics, but a general understanding can help in development and deployment of software. 
Following is a list of tools and concepts used in this template:

- Microservices
- Containers
- Message broker
- Django
- REST
- JWT
- Kubernetes
- Devops, AutoDevOps

## Diagram of this template
![Image](https://osval-do.github.io/repos/microservice-django-template/k8s_diagram.png)

#  Local development

To manually execute the Django application in local mode:
1. Install [python](https://www.python.org/downloads/)
2. Install [virtualenv](https://pypi.org/project/virtualenv/)
3. Create virualenv:
    ```bash
    virtualenv .venv
    ```
4. Activate virtual enviroment:
    ```bash
    source .venv/bin/activate
    ```
5. Install dependiences: 
    ```bash
    pip3 install -r requirements.txt
    ```
6. Collect static files:
    ```bash
    python manage.py collectstatic --noinput
    ```
6. Create the file "local_env.py" in the root folder with the following code:
    ```python
    # Please generate an unique key:
    SECRET_KEY = '%q3&3#hDg7o*=fmj1md6%kvm(_5a9c2)u51gmre((1%w+3nqh!-'
    DATABASE_URL = 'sqlite:///db.sqlite3'
    ALLOWED_HOSTS = "localhost,127.0.0.1"
    DEBUG = True
    AMPQ_URL = None
    ```
7. Run server: 
    ```bash
    python3 manage.py runserver
    ```
## Settings and environment vars

While in development, a local not versioned file is used for adjusting Django settings. This file, named `local_env.py`, is located at the root of the project. If the file doesn't exists the Django will try to load its settings from the OS or container environment. The names of the variables are the same in both cases.

This is the list of the variables:
- `SECRET_KEY`: The key used by Django for encryption of tokens.
- `DATABASE_URL`: A well formed URL for the main database for the microservice.
- `ALLOWED_HOSTS`: A CSV of ips/domains that can access the server.
- `DEBUG`: Enables the debug mode in Django.

# Docker deployment


## Requirements

* A system with Docker installed.

## Testing the container

The dockerfile used to generate a container for the microservice is located in infrastructure/dockerfile. Tools like [minikube](https://minikube.sigs.k8s.io/docs/start/) or [docker desktop](https://www.docker.com/products/docker-desktop/) can be used to test locally the microservice as a container.

This command will generate an image:
```bash
docker build -f infrastructure/dockerfile -t your_microservice_image_name .
```
You can run the image with this command:
```bash
docker run your_microservice_image_name
```
The image can be pushed into a container registry with:
```bash
docker push your_microservice_image_name
```

## Docker compose 
- TODO

# Kubernetes deployment
The following chapters explain the installation and manual use of the kubernetes scripts and configurations contained in the template.

## Requirements
- Access to a kubernetes cluster (where the command `kubectl` is available)
    - For small scale or local development [minikube](https://minikube.sigs.k8s.io/docs/start/) is recommended.
    - A cloud based kubernetes solution can be used for production. 
- A container image registry.
- A configured ingress controller, for example [ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/).
- cert-manager to handle certificates [installation guide](https://cert-manager.io/docs/installation/kubectl/)
- Helm, used for installation and upgrading kubernetes resources. [installation instructions](https://helm.sh/docs/intro/install/)

## Namespaces
A kubernetes namespace is used to isolate this microservice and its resources from other microservices. Not only to prevent collisions with names but for security and management.
An unique namespace and a name should be decided before starting development of a new microservice based on this template.

In the following commands and the rest of this guide the {microservice-space} is used to identify the namespace of the microservice, while {microservice-name} is used to give a recognizable name to the microservice inside its namespace.

The following command will create namespace for the microservice:
```bash
kubectl create namespace {microservice-space}
```

It will also be necessary te create a namespace for common resources that will be shared across all microservices:
```bash
kubectl create namespace {microservice-common}
```

## Secrets
First generate the JWT keys used for authentication. You will need to have installed openssl.
Run the following command to generate a private key (to sign tokens):
```bash
openssl genrsa > private.pem
```
Now generate a public key (to verify tokens):
```bash
openssl rsa -in private.pem -pubout -out public.pem
```
The private key should be kept secured and only exposed to the microservice that will manage the logins.

To securely transfer confidential configurations to running microservices, is necessary to define them in the namespace of the microservice. This secrets will be passed as environment variables. Use this command to generate them:
```bash
kubectl -n={microservice-space} create secret generic {secrets-name} \
  --from-literal=DATABASE_PASSWORD=<POSTGRESQL_PASSWORD> \
  --from-literal=SECRET_KEY=<A_DJANGO_SECRET_KEY> \
  --from-file=JWT_VERIFY_KEY=public.pem \
  --from-file=JWT_SIGN_KEY=0
```

A microservice that manages the login and authorization should be configured with this instead:
```bash
kubectl -n={microservice-space} create secret generic {secrets-name} \
  --from-literal=DATABASE_PASSWORD=<POSTGRESQL_PASSWORD> \
  --from-literal=SECRET_KEY=<A_DJANGO_SECRET_KEY> \
  --from-file=JWT_VERIFY_KEY=public.pem \
  --from-file=JWT_SIGN_KEY=private.pem
```

* Remember change the django secret key for one of you own!
* Replace {secrets-name} with a name of your own

## Helm files
The sub folders under infrastructure/ contain helm templates that will setup the required elements to make the microservice work ina kubernetes cluster. To make this work, first [install helm](https://helm.sh/docs/intro/install/) in the same location where the kubernetes cluster is controlled (where the kubectl command is launched).

* infrastructure/common/ contains the common services and resources used by all microservices based on this template.
* infrastructure/microservice/ is the template that setups this microservice.
* infrastructure/values.yaml are the default variables/parameters required by all the templates.

All files in infrastructure/ can be changed in order to accommodate specific needs by the microservices derived from this repository. 

## Setup values
In order to install in kubernetes trough helm, first create a copy of the infrastructure/values.yaml and store it in infrastructure/local_env.yaml. This file contains the parameters that need to be configured before launching in the kubernetes environment. The explanation of each parameter is included in the file.

## Install or update
To install or update the microservices kubernetes resources use the following command:
```bash
helm upgrade -n {microservice-common} -f infrastructure/local_env.yaml {microservice-common} ./infrastructure/common  -i --create-namespace
helm upgrade -n {microservice-space} -f infrastructure/local_env.yaml {microservice-name} ./infrastructure/microservice -i --create-namespace
```

## Debugging
The default template generates two pods, one with the Django server and the other with a PostgreSQL database.
Their state can be checked with this command:
```bash
kubectl -n={microservice-space} get pods
```
Wich will print a list with the pods in the namespace of our microservice, similar to this one:
```
NAME                                    READY   STATUS    RESTARTS   AGE
microservice-db-depl-5699f8dc4f-vshqz   1/1     Running   0          24m
microservice-dpl-76c78986c4-qsk75      1/1     Running   0          58s
```
The STATUS and RESTARTS columns can tell us if the containers are behaving incorrectly. The next command will print the terminal output of the container (similar to `docker logs` command) and can be used for error diagnostics:
```bash
kubectl -n={microservice-space} logs microservice-dpl-76c78986c4-qsk75
```

### Deleting the microservice resources
For removing the resources created use the following command:
```bash
helm delete {microservice-name}
```
Warning: The command `delete` might not remove data saved in persistent volumes like the one used for PostgreSQL.



# Continuous Integration/Deployment

AutoDevOps comes integrated in this template, but there are some needed configurations to be set depending on where the repository is being hosted.

The next list are the secrets used by the autodevops automation that need to be configured in the repository. If the repository is in GitHub, the secrets need to be configured in Settings>Secrets. In Gitlab this is in Settings>CI/CD>Variables,

|Name | Description  |
| --- | --- |
|IMAGE_NAME|Name of the image that will be generated for the microservice container
|DOCKER_USERNAME|Username for the docker image repository
|DOCKER_PASSWORD|Password for the docker image repository
|DOCKER_SERVER|Address for the image repository (i.e. [dockerhub.com](https://hub.docker.com/) or self hosted)
|MICROSERVICE_NAMESPACE|Namespace given to this microservice
|LETS_ENCRYPT_EMAIL|Email to admin any generated Let's Encrypt certificate 
|MICROSERVICE_NAME|Name to be prefixed to kubernetes resources generated for this microservice
|SECRET_SETTINGS_NAME|Name of the secrets that are shared between the microservices (used as {secrets-name} in the manual)
|DOMAIN_NAME|A DNS name used to access the microservices (required for certificate generation)
|COMMON_NAMESPACE|The name of the namespace with shared services

## Github workflows

The following workflows are included in .github/workflows, you can use them as a basis for your own:

* **.github/workflows/test_backend.yaml** Tests the Django project.
* **deploy_selfhosted_common.yaml** Updates the common services after pushing changes to the helm files. Requires a selfhosted runner.
* **deploy_selfhosted.yaml** Deploys changes to the microservice code to a kubernetes cluster after passing the tests workflow. Requires a selfhosted runner.

## Gitlab pipelines

- TODO


# Backend programming

This template is planned to run amongst other microservices based on this same template. To have an orderly coexistence of the services this Django project comes preconfigured with some tools to help in this endeavour.

## Authentication

To prevent having to start a Django user session in each of the microservices, the library [`djangorestframework-simplejwt`](https://pypi.org/project/djangorestframework-simplejwt/) is used for sharing the session with common JSON web tokens. A single microservice should handle the authentication of users, by giving it a private key (as described in the secrets section of this manual). Your application frontend should use the given JWT when calling any other microservice in the cluster. Other microservices will be configured to use the public part of the key, and will be able to verify the user.

## Communication between services

There are means to make two microservices talk to each other (for example using their ClusterIP service). But a more recommended way is to use the included message broker RabbitMQ, which should be installed in the common namespace. Complex communication can be more easily solved with by sending an receiving event messages.

## Data synchronization

Expanding in the previous topic, this template includes the [`django-cqrs`](https://pypi.org/project/django-cqrs/) library that implements an event system for replicating data across multiple microservices using RabbitMQ. You can find more info about how to use and configure your project in the [documentation](https://django-cqrs.readthedocs.io/en/latest/).
