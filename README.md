# Django microservice template
A template for creating Django microservices that include support for Docker, Kubernetes, CI/CD, data synchronization and more!

## When to use this template
A microservice based on this template can help solve two different situations:
a- In the 

# Usage instructions

## Local development
To execute the project in local mode:
1. Install [python](https://www.python.org/downloads/)
2. Install [virtualenv](https://pypi.org/project/virtualenv/)
3. Create virualenv: `virtualenv venv`
4. Activate virtual enviroment: `source venv/bin/activate`
5. Install dependiences: `pip3 install -r requirements.txt`
6. Create the file "local_env.py" in the root folder with the following code:
```python
# Please generate an unique key:
SECRET_KEY = '%q3&3#hDg7o*=fmj1md6%kvm(_5a9c2)u51gmre((1%w+3nqh!-'
DATABASE_URL = 'sqlite:///db.sqlite3'
ALLOWED_HOSTS = "localhost,127.0.0.1"
DEBUG = True
```
7. Run server: `python3 manage.py runserver`

## Docker

### Manually build container
If there is a docker environment where the repository is located, you can build the container with the following command:
```bash
docker build -f infrastructure/dockerfile .
```

### Push image
You can generate an image of the microservice 

## Kubernetes deployment



## Continuous Integration/Deployment

### Github workflows

### Gitlab pipelines


# Backend programming

## 