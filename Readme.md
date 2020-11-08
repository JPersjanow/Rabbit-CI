# Rabbit-CI Backend
#### Manage and Automate

[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/JPersjanow/Rabbit-CI.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/JPersjanow/Rabbit-CI/context:javascript) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/JPersjanow/Rabbit-CI.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/JPersjanow/Rabbit-CI/context:python) [![Total alerts](https://img.shields.io/lgtm/alerts/g/JPersjanow/Rabbit-CI.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/JPersjanow/Rabbit-CI/alerts/)

Rabbit-CI is an automation server linked with project managment web app.
Backend was written in Python, using Flask library

### Tech

Rabbit uses a number of open source projects to work properly:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask_restplus](https://flask-restplus.readthedocs.io/en/stable/)

And of course Rabbit itself is open source with a [public repository](https://github.com/JPersjanow/Rabbit-CI) on GitHub.

### Installation and deployment

* Back-end deployment
1) First install required Python packages from requirements file
```
pip install -r backend/requirements.txt
```
2) Run directory_creator.py with proper options
```
python3 backend/directory_creator.py 
    --installation_directory <directory to install rabbit>
```
3) Start server
```
python3 backend/rabbit_api_server.py
```
4) /*/ If server doesn't start or there is any problems with endpoints make sure RABBITCONFIG environmental variable is set to installation directory

# Project team
[Jakub Persjanow](https://github.com/JPersjanow) / [Alicja Szymikowska](https://github.com/szal03) / [Julia Wenta](https://github.com/juliawenta)
