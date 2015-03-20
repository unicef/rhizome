# fabricfile to deploy build
#
# depends on installation of fabric - pip install fabric
#
# example invocation
# $ fab -H jenkins@uf04.seedscientific.com deploy

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
    work_path = '~/polio'
    venv_path = '/tmp/venv'

    backend_path = '/tmp/polio-backend/'
    frontend_path = '/tmp/polio-frontenv/'

    ###
    ### on build machine...
    ###

    # set up dependencies
    print ("TODO: confirm build machine has dependencies. i.e. node, gulp.")
    # e.g.
    # sudo gem install sass
    # sudo gem install compass

    # enter virtual environment
    make_virtualenv(venv_path)
    with virtualenv(venv_path):
        local ("pip install -r requirements.txt")

        # make dist
        local("./node_modules/.bin/bower install")
        local("./node_modules/.bin/gulp dist")

    ###
    ### on target machine...
    ###

    # make folder if it doesn't exist
    run ("mkdir -p %s" % work_path)

    # push to remote server
    put ('dist/uf04-frontend.zip', work_path)
    put ('dist/uf04-backend.zip', work_path)

    # unzip stuff
    with cd(work_path):
        run("unzip uf04-frontend.zip -d %s" % frontend_path)
        run("unzip uf04-backend.zip -d %s" % backend_path)

    # in front-end path
    # with cd(frontend_path):
    #     run("chown -R www-data:www-data .")
    #
    # # in server path -
    # with cd(backend_path):
    #     run("pip install -r requirements.txt")
    #
    #     # echo "== SYNCDB / MIGRATE =="
    #     run("python manage.py syncdb --settings=polio.prod_settings")
    #     run("python manage.py migrate --settings=polio.prod_settings")
    #
    #     # echo "== BUILDING DATABASE =="
    #     run("bash bin/build_db.sh")

    # bounce apache??
    # customize any other configuration?
    #
    # echo "== BUILDING DOCUMENTATION ==" # maybe...
    # make clean -C docs
    # make html -C docs
    #
    # echo "== RUNNING TESTS =="
    # python manage.py test datapoints.tests.test_cache --settings=polio.settings_test

# def prepare_deploy():
    # local("pip install -r requirements.txt")

    # from shell script
    # git pull origin development
    # pip install -r requirements.txt
    # python manage.py syncdb --settings=polio.prod_settings
    # python manage.py migrate --settings=polio.prod_settings
    # bash bin/build_db.sh
