import unittest
import yaml

from fabric.api import local, run, execute, task
from fabric.context_managers import lcd, cd, settings, hide
from fabric.contrib.files import append

from gitsynclib.GitSync import GitSync
from gitsynclib.GitNotified import GitNotified

host = '10.10.10.11'

text_1 = """Nullam id dolor id nibh ultricies vehicula ut id elit.
Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum.
"""

text_2 = """Sed posuere consectetur est at lobortis. Integer posuere erat a
ante venenatis dapibus posuere velit aliquet. """

text_3 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras
justo odio, dapibus ac facilisis in, egestas eget quam. Vivamus sagittis lacus
vel augue laoreet rutrum faucibus dolor auctor. Etiam porta sem malesuada
magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit.
"""

config_yaml = """
local_path: /vagrant/scratch
local_branch: unittesting
remote_host: {0}
remote_user: vagrant
remote_path: /home/vagrant/scratch
""".format(host)

@task
def setup_remote_project():
    delete_remote_repo()
    run( 'mkdir /home/vagrant/scratch' );
    with cd('/home/vagrant/scratch'):
        run("touch one.txt")
        run("touch two.txt")
        run("touch three.txt")

        append('one.txt', text_1)
        append('two.txt', text_2)
        append('three.txt', text_3)


@task
def delete_remote_repo():
    run("rm -Rf /home/vagrant/scratch")

@task
def delete_local_repo():
    local("rm -Rf /vagrant/scratch")

@task
def update_yaml():
    with lcd('/vagrant'):
        local("echo '{0}' > scratch.yaml".format(config_yaml))

class GitSyncTest(unittest.TestCase):

    def setUp(self):
        self.host = host
        update_yaml()
        execute(
            setup_remote_project,
            hosts=[host],
        )

    def tearDown(self):
        execute(
            delete_remote_repo,
            hosts=[host],
        )
        execute(
            delete_local_repo,
            hosts=[host],
        )

    def get_git_sync(self):
        notifier = GitNotified()

        config_stream = open("/vagrant/scratch.yaml", 'r')
        config = yaml.safe_load(config_stream)

        git_sync = GitSync(config, notifier)

        return git_sync
