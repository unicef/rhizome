# example invocation
# $ fab -H ubuntu@xx.x.xxx.xx deploy -i ~/.ssh/some.key
# Fabfile to automate the installation process!

from fabric.api import local, run, cd, put, env, sudo
from fabtools import require

# database, username and password
env.database = 'afg_polio'
env.username = 'djangoapp'
env.password = 'anythinghere'


env.use_ssh_config = True
# this can be set by passing venv_path arg to deploy() target
local_venv_path = None

# /var/www/clients.seedscientific.com/uf/UF04
remote_work_path = 'deploy/rhizome-work'
remote_backend_path = '/var/www/apps/rhizome/'
remote_frontend_path = '/var/www/apps/rhizome/webapp/public/static/'
remote_manage_path = remote_backend_path + "manage.py"

# deploy build
# build-machine dependencies - node, gulp, bower, sass, compass, ruby, virtualenv, fabric-virtualenv

def new_machine(venv_path=None):
    global local_venv_path
    local_venv_path = venv_path;

    # Local machine

    # Remote machine
    update_remote()
    instal_basic_packages()
    install_postgres()
    configure_psql()
    install_apache()
    create_dirs()

# setup is doing test and pushing it to the remote
def deploy():
    '''
    '''
    # run_tests()
    # _build_dependencies()
    _push_to_remote()

# update the remote server
def update_remote():
    sudo('apt-get update')
# install basic packages such as unzip, python-dev, pip, build-essential.
def instal_basic_packages():
    sudo('apt-get install -y unzip python-pip python-dev build-essential python-psycopg2 libpq-dev')
# install postgresql
def install_postgres():
    sudo('apt-get install -y postgresql postgresql-contrib')
# create postgresql user and Database
def configure_psql():
    require.postgres.user('djangoapp', password='testpass', superuser=True, createdb=True, createrole=True, connection_limit=20)
    require.postgres.database('afg_polio', owner='djangoapp')
    # for restart: sudo('service postgresql restart')
# install apache
def install_apache():
    #sudo('apt-get install -y apache2')
    sudo('apt-get install -y libapache2-mod-wsgi')
# install virtualenv and virtualenvwrapper
def install_virtualenv():
    sudo('pip install virtualenv virtualenvwrapper')

# create directories structure
def create_dirs():
    require.directory(remote_work_path, owner='www-data', use_sudo=True)
    require.directory(remote_backend_path, owner='www-data', use_sudo=True)
    require.directory(remote_frontend_path, owner='www-data', use_sudo=True)
    # set the read_write permission on the directory www to normal users as well
    run('sudo chmod -R ugo+rw /var/www/')
    restart_apache()

# apache controls
def stop_apache():
    run("sudo service apache2 stop")

def start_apache():
    run("sudo service apache2 start")

def restart_apache():
    run("sudo service apache2 restart")


def run_tests():

    local("coverage run manage.py test --settings=rhizome.settings.test")
    local("coverage html --omit='*venv/*,*migrations/*,*admin*,*manage*,*wsgi*,*__init__*,*test*,*settings*,*url*' -i")


# build dependencies
def _build_dependencies():
    ### on build machine ###

    # only build with a virtualenv if one is passed in.
    if (local_venv_path):
        # make virtual env
        local('virtualenv %s' % local_venv_path)

        # enter virtual environment
        activate_this_file = "%s/bin/activate_this.py" % local_venv_path
        execfile(activate_this_file, dict(__file__=activate_this_file))

    # update/install dependencies
    local("cd webapp && npm install")

    # build fe and package the project
    # with NODE_ENV=production, uglify have be done.
    local("cd webapp && npm run package")

# push build to remote
def _push_to_remote():
    ### on target machine ###

    # make folder if it doesn't exist #
    #run ("mkdir -p %s" % remote_work_path)

    # push to remote server #
    #put ('dist/rhizome.zip', remote_work_path, use_sudo=True)

    # unzip stuff #
    #with cd(remote_work_path):

        # Delete all Python, HTML, and SQL files. We don't delete the entire
        # directory because that will catch the media/ directory which will
        # probably have files we want to keep in it. This way we ensure that we
        # clean out old scripts before deploying. Set mindepth to 2 so that we
        # can keep the server's settings.py file in the application folder

        # [these unzips were trying to overwrite .pyc files owned by www-root
        #  so the 'find' command above may not be deleting enough compiled pycs]
        # when the unzip fe files will be included

        ## dont think this is avtually overwriting
        #run("unzip -o rhizome.zip -d %s" % remote_backend_path)

    # in server path -
    with cd(remote_backend_path):
        # remove both compiled files
        # run('sudo rm -rf `find . -name "*.pyc*"`')
        #
        # # install python dependencies
        # sudo("pip install -r requirements.txt")

        # echo "== SYNCDB / MIGRATE =="

        # run("bash setEnvi.b")
        # add environment variables
        # run("source env_var/environment_seed.env")

        # run("export DB_PASSWORD=myPassword")
        run("source env_var/environment_seed.env && python manage.py migrate --settings=rhizome.settings.production")

        # echo "== COLLECT STATIC =="
        run("source env_var/environment_seed.env && python manage.py collectstatic --noinput --settings=rhizome.settings.production")

        # add waffle_switch pdf for exporting pdf
        # run("./manage.py waffle_switch pdf on --create --settings=settings")
        # run("./manage.py waffle_switch image on --create --settings=settings")

        ## building documentation ##
        # run("cd docs/ && make clean && make html")

        # echo "== RUNNING TESTS =="
        # run("python manage.py test datapoints.tests.test_api --settings=rhizome.settings.test")
