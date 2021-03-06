import datetime
import json
import os

from fabric import api, operations, contrib
from fabric.state import env

ENVIRONMENTS = {
    "prd": {
        "hosts": 'int-elex-prd-east.newsdev.net'
    }, 
    "stg": {
        "hosts": 'int-elex-stg-east.newsdev.net'
    },
    "prd-west": {
        "hosts": 'int-elex-prd-west.newsdev.net'
    }, 
    "stg-west": {
        "hosts": 'int-elex-stg-west.newsdev.net'
    }
}

env.project_name = 'elex-ftp-loader'
env.user = "ubuntu"
env.forward_agent = True
env.branch = "master"

env.racedate = os.environ.get('RACEDATE', None)
env.hosts = ['127.0.0.1']
env.dbs = ['127.0.0.1']
env.settings = None

@api.task
def r(racedate):
    env.racedate = racedate

@api.task
def development():
    """
    Work on development branch.
    """
    env.branch = 'development'

@api.task
def master():
    """
    Work on stable branch.
    """
    env.branch = 'master'

@api.task
def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name

@api.task
def e(environment):
    env.settings = environment
    env.hosts = ENVIRONMENTS[environment]['hosts']

@api.task
def clone():
    api.run('git clone git@github.com:newsdev/%(project_name)s.git /home/ubuntu/%(project_name)s' % env)

def mkvirtualenv():
    api.run('mkvirtualenv %(project_name)s' % env)

@api.task
def pull():
    api.run('cd /home/ubuntu/%(project_name)s; git fetch; git pull origin %(branch)s' % env)

@api.task
def pip_install():
    api.run('cd /home/ubuntu/%(project_name)s; workon %(project_name)s && pip install -r requirements.txt; python setup.py install' % env)

@api.task
def setup():
    clone()
    mkvirtualenv()
    pip_install()

@api.task
def deploy():
    pull()
    pip_install()
