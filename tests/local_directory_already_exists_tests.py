from fabric.api import local, run, execute, task
from fabric.context_managers import lcd, cd, settings, hide

from testcase import GitSyncTest

class LocalDirectoryAlreadyExistsTest(GitSyncTest):

    def setUp(self):
        super(LocalDirectoryAlreadyExistsTest, self).setUp()
        with lcd( '/vagrant' ):
            local('mkdir scratch')

    def tearDown(self):
        super(LocalDirectoryAlreadyExistsTest, self).tearDown()
        with lcd( '/vagrant' ):
            wc_output = local('ls -1d scratch | wc -l', True)
            number_of_files = int(wc_output.stdout)
            if number_of_files > 0:
                local('rmdir scratch')

    def existing_local_directory_test(self):
        with settings(hide('warnings', 'running', 'stdout', 'stderr')):
            try:
                git_sync = self.get_git_sync()
                git_sync.run_initial_sync()
            except Exception as e:
                self.assertTrue(
                    False,
                    "Running initial sync threw and exception: {0}".format(e)
                )


class LocalDirectoryAlreadyExistsWithGitRepoTest(GitSyncTest):

    def setUp(self):
        super(LocalDirectoryAlreadyExistsWithGitRepoTest, self).setUp()
        with settings(hide('warnings', 'running', 'stdout', 'stderr')):
            with lcd( '/vagrant' ):
                local('mkdir scratch')
            with lcd( '/vagrant/scratch' ):
                local( 'git init' )

    def tearDown(self):
        super(LocalDirectoryAlreadyExistsWithGitRepoTest, self).tearDown()
        with lcd( '/vagrant' ):
            wc_output = local('ls -1d scratch | wc -l', True)
            number_of_files = int(wc_output.stdout)
            if number_of_files > 0:
                local('rm -Rf scratch')

    def existing_local_directory_with_git_repo_test(self):
        with settings(hide('warnings', 'running', 'stdout', 'stderr')):
            git_sync = self.get_git_sync()
            with self.assertRaises(Exception):
                git_sync.run_initial_sync()
