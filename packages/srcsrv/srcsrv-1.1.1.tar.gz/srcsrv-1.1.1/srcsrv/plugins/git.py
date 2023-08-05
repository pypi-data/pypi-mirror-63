'''Git plugin
'''
# Python modules
import os
import sys
import git
import argparse
# Source index modules
from .. import base


class Git(base.Base):
    '''Git processing
    '''
    def __init__(self, args, namespace):
        super(Git, self).__init__(namespace)

        # Add plugin specific arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-I', '--uri',    help='Git repository server URI', default='github.com')
        parser.add_argument('-X', '--hexsha', help='Git repository branch hash')
        # Pares remaining  unrecognized args
        namespace = parser.parse_args(args)
        self.args.__dict__.update(namespace.__dict__)
        try:
            if not self.args.hexsha or len(self.args.hexsha) != 40:
                raise ValueError
            int(self.args.hexsha, 16)
        except ValueError:
            self.repo = git.Repo(self.args.build_base)
            self.args.hexsha = self.repo.active_branch.object.hexsha

    def process(self, src=None, code=None, md5=None):
        ''' Process .PDB content
        '''
        if not src:
            # called without arguments; Print SRCSRV variables block
            self.args.output.write(rf'''SRCSRVTRG=%git_extract_target%
SRCSRVCMD=%git_cmd%
GIT_EXTRACT_TARGET=%git_cache%\%fnbksl%(%git_branch%)%fnbksl%(%var2%)\%var3%\%fnfile%(%var2%)
GIT_CMD=%git_exe% -H "Accept: application/vnd.github.v3.raw" %git_creds% -L %git_url%%var2% --create-dirs -o %SRCSRVTRG%
GIT_EXE=curl.exe
GIT_URL=%git_scheme%%git_login%{self.args.uri}/raw/%git_branch%/%git_hexsha%
GIT_SCHEME={self.args.scheme}
GIT_BRANCH={self.args.branch}
GIT_HEXSHA={self.args.hexsha}
GIT_CACHE=%userprofile%
GIT_LOGIN=%github_token%
GIT_CREDS=%github_creds%
''')
            return True

        # called with source file path; Print SRCSRV file entry
        self.args.output.write(f'{src}*{code.path}*{md5}\n')
        return True


__all__ = ['Git']
