import fabric.contrib.files
from fabric.api import local, run, execute, task
from fabric.context_managers import lcd, cd, settings, hide

from testcase import GitSyncTest

class ChangesTest(GitSyncTest):

    @task
    def check_local_change_on_server(self):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            with cd('/home/vagrant/scratch'):

                self.assertTrue(fabric.contrib.files.exists("one.txt"))

                self.assertTrue(
                    fabric.contrib.files.contains(
                        "one.txt",
                        "Now is the winter of our discontent."
                    )
                )

                self.assertFalse(
                    fabric.contrib.files.contains(
                        "one.txt",
                        "beware the ides of march"
                    )
                )

    def local_changes_test(self):

        with settings(hide('warnings', 'running', 'stdout', 'stderr')):

            git_sync = self.get_git_sync()
            git_sync.run_initial_sync()

            with open("/vagrant/scratch/one.txt", "a") as file_one:
                file_one.write("Now is the winter of our discontent.")
                file_one.close()

            git_sync.run_sync()

            execute(self.check_local_change_on_server,self,hosts=[self.host],)
