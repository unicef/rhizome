# Rhizome
Designed for data visualization to help eradicate polio!

Built with Python, Django, JavaScript, React, Reflux, HighCharts, and many other libraries.

# Up and Running for Developers

## Setting up the development environment with Docker #

Prerequisites

1. VirtualBox
http://download.virtualbox.org/virtualbox/5.0.26/VirtualBox-5.0.26-108824-OSX.dmg

Install Docker Machine. In Mac OS X you could install via `brew`

2. Docker Toolbox
https://www.docker.com/products/docker-toolbox

```
$ brew install docker-machine docker-compose
```
Initialize Docker environment

```
$ docker-machine create -d virtualbox dev
$ docker-machine start dev
```
Add `eval "$(docker-machine env dev)"` into .bash_profile

In Mac OS X, forward the port to host

```
$ VBoxManage controlvm dev natpf1 "django,tcp,127.0.0.1,8000,,8000"
```
<!-- Navigate to repository directory, de-comment Line.8 `ENV CHINESE_LOCAL_PIP_CONFIG="--index-url http://pypi.douban.com/simple --trusted-host pypi.douban.com"` to use Chinese pip mirror. -->

Run

```
$ docker-compose build && docker-compose up
```

Enter Docker Web Server Container running Django

```
$ docker exec -it rhizome_rhizome_1 bash
```

Enter Docker DB Container running Postgres

```
docker exec -it rhizome_db_1 psql -U postgres
```

# Documentation
Start here by checking out our [documentation](http://unicef.github.io/rhizome/).

# Style
For python style guide and instructions on how to configure your editor in alignment with our linter config see the [plylintrc file](https://github.com/unicef/rhizome/blob/dev/rhizome/pylintrc)
