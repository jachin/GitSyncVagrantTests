from fabric.api import local, run, execute, task
from fabric.context_managers import lcd, cd, settings, hide

from testcase import GitSyncTest

class GitSyncInitTest(GitSyncTest):

    @task
    def simple_change(self):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            with cd('/home/vagrant/scratch'):
                self.assertTrue(run("ls one.txt").succeeded)
                self.assertTrue(run("ls not_real.txt").failed)

    def run_initial_sync_test(self):

        git_sync = self.get_git_sync()
        git_sync.run_initial_sync()

        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            with lcd('/vagrant/scratch'):
                self.assertTrue(local("ls one.txt").succeeded)
                self.assertTrue(local("ls not_real.txt").failed)

        execute(self.simple_change,self,hosts=[self.host],)
