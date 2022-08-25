

# Usage instructions

## Local development
To execute the project in local mode:
1. Install [python](https://www.python.org/downloads/)
2. Install [virtualenv](https://pypi.org/project/virtualenv/)
3. Create virualenv: `virtualenv venv`
4. Install dependiences: `pip3 install -r requirements.txt`
5. Create the file "local_env.py" in the root folder with the following code:
```python
# Please generate an unique key:
SECRET_KEY = '%q3&3#hDg7o*=fmj1md6%kvm(_5a9c2)u51gmre((1%w+3nqh!-'
DATABASE_URL = 'sqlite:///db.sqlite3'
ALLOWED_HOSTS = "localhost,127.0.0.1"
DEBUG = True
```
6. Run server: `python3 manage.py runserver`

## Manually build container
If there is a docker environment where the repository is located, you can build the container with the following command:
`docker build -f infrastructure/dockerfile .`