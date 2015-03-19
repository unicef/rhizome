# fabricfile to deploy build
#
# depends on installation of fabric - pip install fabric
#
# example invocation
# $ fab -H jenkins@uf04.seedscientific.com fabfile.py


# fab hello:name=Elliot
def hello(name="world"):
    print("Hello %s!" % name)

from fabric.api import local, run, cd, put
from fabvenv import virtualenv, make_virtualenv

# test build
#
# test-machine dependencies - python, pip, postgres
#
def test():
    local("echo TODO: do tests here")

# deploy build
#
# build-machine dependencies - node, gulp, bower, sass, compass, ruby, virtualenv, fabric-virtualenv
def deploy():
    # /var/www/clients.seedscientific.com/uf/UF04
    code_dir = '~/polio'

    # set up dependencies
    print ("TODO: confirm build machine has dependencies. i.e. node, gulp.")
    # sudo gem install sass
    # sudo gem install compass

    # enter virtual environment
    # local ("virtualenv /tmp/venv") # we may be able to save space and time
    venv_path = '/tmp/venv'
    make_virtualenv(venv_path)
    with virtualenv(venv_path):
        local ("pip install -r requirements.txt")

        # make dist
        local("./node_modules/.bin/bower install")
        local("./node_modules/.bin/gulp dist")

    # put dist
    put ('dist/uf04-frontend.zip', code_dir)
    put ('dist/uf04-backend.zip', code_dir)

    # make folder if it doesn't exist
    # run ("mkdir -p %s" % code_dir)


    # with cd(code_dir):
        # run("touch fab.test")

# deploy -
def

# def prepare_deploy():
    # local("pip install -r requirements.txt")

    # from shell script
    # git pull origin development
    # pip install -r requirements.txt
    # python manage.py syncdb --settings=polio.prod_settings
    # python manage.py migrate --settings=polio.prod_settings
    # bash bin/build_db.sh
