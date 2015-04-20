# fabricfile to deploy build
#
# depends on installation of fabric - pip install fabric virtualenv
#
# example invocation
# $ fab -H jenkins@uf04.seedscientific.com deploy
# $ fab -H ubuntu@52.0.138.67 deploy
# $ fab -H ubuntu@uf04.seedscientific.com deploy

from fabric.api import local, run, cd, put

## global variables
##

# this can be overwritten by passing venv_path arg to deploy() target
local_venv_path = '/tmp/venv'

# /var/www/clients.seedscientific.com/uf/UF04
remote_work_path = '~/deploy/polio-work'
remote_backend_path = '/var/www/apps/polio/'
remote_frontend_path = '/var/www/polio/static/'

# deploy build
#
# build-machine dependencies - node, gulp, bower, sass, compass, ruby, virtualenv, fabric-virtualenv
def deploy(venv_path=None):
    global local_venv_path
    local_venv_path = venv_path;

    # on local machine...
    _build_dependencies()

    # on target machine
    stop_apache()
    _push_to_remote()
    start_apache()

# apache controls
def stop_apache():
    run("sudo /etc/init.d/apache2 stop")

def start_apache():
    run("sudo /etc/init.d/apache2 start")


# build dependencies
#
#
def _build_dependencies():
    ###
    ### on build machine...
    ###

    # set up dependencies
    print ("TODO: confirm build machine has dependencies. i.e. node, gulp.")
    # e.g.
    # sudo gem install sass
    # sudo gem install compass

    # only build with a virtualenv if one is passed in.
    if (local_venv_path):
        # make virtual env
        local('virtualenv %s' % local_venv_path)

        # enter virtual environment
        activate_this_file = "%s/bin/activate_this.py" % local_venv_path
        execfile(activate_this_file, dict(__file__=activate_this_file))

    # update/install dependencies
    local ("npm install")
    local ("pip install -r requirements.txt")

    # make dist
    local("./node_modules/.bin/bower install")
    local("./node_modules/.bin/gulp dist")

# push build to remote
#
#
def _push_to_remote():
    ###
    ### on target machine...
    ###

    # make folder if it doesn't exist
    run ("mkdir -p %s" % remote_work_path)

    # push to remote server
    put ('dist/uf04-frontend.zip', remote_work_path)
    put ('dist/uf04-backend.zip', remote_work_path)

    # unzip stuff
    with cd(remote_work_path):
        run("rm -rf %s" % remote_frontend_path)

        # Delete all Python, HTML, and SQL files. We don't delete the entire
        # directory because that will catch the media/ directory which will
        # probably have files we want to keep in it. This way we ensure that we
        # clean out old scripts before deploying. Set mindepth to 2 so that we
        # can keep the server's settings.py file in the application folder
        run("find %s -mindepth 2 -regextype 'posix-extended' -regex '.*\.(pyc?|sql|html) -delete'" % remote_backend_path)

        # [these unzips were trying to overwrite .pyc files owned by www-root
        #  so the 'find' command above may not be deleting enough compiled pycs]
        run("unzip -o uf04-frontend.zip -d %s" % remote_frontend_path) # -o is overwrite
        run("unzip -o uf04-backend.zip -d %s" % remote_backend_path)

    with cd(remote_frontend_path):
        # remove compiled files
        run('sudo rm -rf `find . -name "*.pyc"`')

        # chgroup, chmod so apache can edit
        run('chgrp -R www-data *')
        run('chmod -R g+w *')

    # in server path -
    with cd(remote_backend_path):
        # remove compiled files
        run('sudo rm -rf `find . -name "*.pyc"`')

        run("chgrp -R www-data *")
        run("chmod -R g+w *")

        run("pip install -r requirements.txt")

        # echo "== SYNCDB / MIGRATE =="
        run("python manage.py syncdb --noinput")
        run("python manage.py migrate --noinput")

        # echo "== BUILDING DATABASE =="
        run("bash bin/build_db.sh")

    # bounce apache??
    # customize any other configuration?
    #
    # echo "== BUILDING DOCUMENTATION ==" # maybe...
    # make clean -C docs
    # make html -C docs
    #
    # echo "== RUNNING TESTS =="
    # python manage.py test datapoints.tests.test_cache --settings=polio.settings_test
