from fabric.api import local, run, execute, task
from fabric.context_managers import lcd, cd, settings, hide

from testcase import GitSyncTest, host, update_yaml, setup_remote_project

class BadLocalPathTest(GitSyncTest):

    def setUp(self):
        self.host = host

        config_yaml = """
        local_path: /Some/Place/Stupid
        local_branch: unittesting
        remote_host: {0}
        remote_user: vagrant
        remote_path: /home/vagrant/scratch
        """.format(host)

        update_yaml(config_yaml)
        execute(
            setup_remote_project,
            hosts=[host],
        )

    def config_check_test(self):

        git_sync = self.get_git_sync()
        with settings(hide('warnings', 'running', 'stdout', 'stderr', 'aborts'), warn_only=True):
            self.assertRaises(SystemExit, git_sync.run_initial_sync)


class BadRemotePathTest(GitSyncTest):

    def setUp(self):
        self.host = host

        config_yaml = """
        local_path: /vagrant/scratch
        local_branch: unittesting
        remote_host: {0}
        remote_user: vagrant
        remote_path: /Some/Place/Stupid
        """.format(host)

        update_yaml(config_yaml)
        execute(
            setup_remote_project,
            hosts=[host],
        )

    def config_check_test(self):

        git_sync = self.get_git_sync()

        output_to_hide = [
            'warnings',
            'running',
            'stdout',
            'stderr',
            'aborts'
        ]

        with settings(hide(*output_to_hide), warn_only=True):
            self.assertRaises(SystemExit, git_sync.run_initial_sync)

class GoodPathsTest(GitSyncTest):

    def config_check_test(self):

        git_sync = self.get_git_sync()

        output_to_hide = [
            'warnings',
            'running',
            'stdout',
            'stderr',
        ]

        with settings(hide(*output_to_hide), warn_only=True):
            git_sync.run_initial_sync()
