# Django microservice template
A template for creating Django microservices that include support for Docker, Kubernetes, CI/CD, data synchronization and more!

This repository contains a template that can be used or aid in the following situations:
- Building a system developed by multiple teams. Each responsible for their own microservice.
- Developing a complex system based on individual modules.
- Add resiliency in deployment, by only updating parts of a system and having lose connection between microservices.
- Automatic management of deployment and scaling.

# Usage instructions

## Local development
To execute the project in local mode:
1. Install [python](https://www.python.org/downloads/)
2. Install [virtualenv](https://pypi.org/project/virtualenv/)
3. Create virualenv:
    ```bash
    virtualenv venv
    ```
4. Activate virtual enviroment:
    ```bash
    source venv/bin/activate
    ```
5. Install dependiences: 
    ```bash
    pip3 install -r requirements.txt
    ```
6. Create the file "local_env.py" in the root folder with the following code:
    ```python
    # Please generate an unique key:
    SECRET_KEY = '%q3&3#hDg7o*=fmj1md6%kvm(_5a9c2)u51gmre((1%w+3nqh!-'
    DATABASE_URL = 'sqlite:///db.sqlite3'
    ALLOWED_HOSTS = "localhost,127.0.0.1"
    DEBUG = True
    ```
7. Run server: 
    ```bash
    python3 manage.py runserver
    ```
### Settings and environment vars

While in development, a local not versioned file is used for adjusting Django settings. This file, named `local_env.py`, is located at the root of the project. If the file doesn't exists the Django will try to load its settings from the OS or container environment. The names of the variables are the same in both cases.

This is the list of the variables:
- `SECRET_KEY`: The key used by Django for encryption of tokens.
- `DATABASE_URL`: A well formed URL for the main database for the microservice.
- `ALLOWED_HOSTS`: A CSV of ips/domains that can access the server.
- `DEBUG`: Enables the debug mode in Django.

### Testing the docker container

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

## Kubernetes deployment
The following chapters explain the installation and manual use of the kubernetes scripts and configurations contained in the template.

### Installation
A cloud based kubernetes solution can be used for production. For small scale or local development [minikube](https://minikube.sigs.k8s.io/docs/start/) is recommended.

### Namespaces
A kubernetes namespace is used to isolate this microservice and its resources from other microservices. Not only to prevent collisions with names but for security and management.
An unique namespace should be decided before starting development a new microservice based on this template.

In the following commands the {microservice-space} is used to identify this name, this needs to be replaced by yours.

The following command will create namespace for the microservice:
```bash
kubectl create namespace {microservice-space}
```

### Secrets
To securely transfer confidential configurations to running microservices, is necessary to define them in the namespace of the microservice. This secrets will be passed as environment variables. Use this command to generate them:
```bash
kubectl -n={microservice-space} create secret generic m8e-settings \
  --from-literal=DATABASE_PASSWORD=psqlpass \
  --from-literal=SECRET_KEY='%q3&3#hDg7o*=fmj1md6%kvm(_5a9c2)u51gmre((1%w+3nqh!-'  
```


### Generate the resources
To manually generate the microservices kubernetes resources use the following command:
```bash
kubectl -n={microservice-space} apply -f infrastructure/k8s_microservice.yaml
```

### Rollout changes to code
If the code has changed, the image of the container needs to be built again. Use the commands explained in "Testing the docker container". Once uploaded to the image registry server execute the following command to refresh the pods running your microservice:
```bash
kubectl -n={microservice-space} rollout restart deployment microservice-dpl
```

### Debugging
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
kubectl -n={microservice-space} delete -f infrastructure/k8s_microservice.yaml
```
Warning: The command `delete` might not remove data saved in persistent volumes like the one used for PostgreSQL.

## Continuous Integration/Deployment

### Github workflows

### Gitlab pipelines


# Backend programming

## Authorization and logins

## Message bus

## Data synchronization

## Scheduled jobs