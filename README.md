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

While inside the docker web instance, create a superuser in order to login

```
root@4d3814881439:/rhizome# ./manage.py createsuperuser
```

To Enter Docker DB Container running Postgres

```
$ docker exec -it rhizome_db_1 psql -U postgres
```

Now that you have the application running, we will need to do a bit more work in
order to be able to compile the front end assets.  

As a note, we inherited this project that was built on an old version of react that we are working on transitioning.  So, unfortunately for now, there are two front end builds that need to be maintained in order for

In the future, all of the front end logic, assets etc will be handled within the react app, and furthermore, this autoload webpack process we be handled by a 3rd container so that developers will not need to run this separately ( [see here](https://hharnisc.github.io/2015/09/16/developing-inside-docker-containers-with-osx.html) for an idea as to how this might work ).

So in order to get the OLD .js working,  

```
$ cd webapp
$ npm install
$ gulp dev
```

And in order to get the NEW .js working,  

```
$ cd react_app
$ npm install
$ webpack -d
```


# Documentation
Start here by checking out our [documentation](http://unicef.github.io/rhizome/).

# Style
For python style guide and instructions on how to configure your editor in alignment with our linter config see the [plylintrc file](https://github.com/unicef/rhizome/blob/dev/rhizome/pylintrc)
