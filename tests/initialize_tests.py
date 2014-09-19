from fabric.api import local, run, execute, task
from fabric.context_managers import lcd, cd, settings, hide

from TestCase import GitSyncTest

class GitSyncTest(GitSyncTest):

    @task
    def simple_change(self):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            with cd('/home/vagrant/scratch'):
                self.assertTrue(True)
                self.assertTrue(run("ls one.txt").succeeded)
                self.assertTrue(run("ls not_real.txt").failed)

    def test_simple_change(self):

        git_sync = self.get_git_sync()
        git_sync.run_initial_sync()

        execute(self.simple_change,self,hosts=[self.host],)
