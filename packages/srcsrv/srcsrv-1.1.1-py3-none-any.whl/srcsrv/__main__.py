'''Scrip for source indexing McAfee builds
Author: Uri Mann
email: abba.mann@gmail.com
@IMPORTANT: Requires Python version 3.6 or above
'''
# Python modules
import os
import sys
import enum
import argparse
import importlib
# Source index modules
from . import indexer


def main(argv=sys.argv[1:]):
    class ArgumentParser(argparse.ArgumentParser):
        '''Arguments parsing class
        '''
        def convert_arg_line_to_args(self, arg_line):
            '''Configuration file loader
            '''
            return arg_line.split()

        def parse_known_args(self, args=None, namespace=None):
            '''Parse common arguments and pass remaining args
               to plugin for parsing
            '''
            namespace, args = super(ArgumentParser, self).parse_known_args(args, namespace)
            if len(args) == 0:
                # No plugin specific arguments found
                return namespace, args

            # Validate plugin class
            try:
                module, klass = namespace.plugin.rsplit('.', 1)
                mdl = importlib.import_module(module)
                namespace.plugin = getattr(mdl, klass)
            except ValueError as err:
                error = f'{args.plugin} does not look like a module path'
                raise ImportError(error) from err
            except AttributeError as err:
                error = f'Module {module} does not define a {klass} attribute/class'
                raise ImportError(error) from err

            # Instantiate plugin which will pares specific argument onto 'namespace'
            namespace.plugin = namespace.plugin(args, namespace)
            return namespace, []

    class Action(enum.IntEnum):
        '''Action type enumeration
        '''
        INDEX = 1
        REINDEX = 2

        # magic methods for argparse compatibility

        def __str__(self):
            return self.name.lower()

        def __repr__(self):
            return str(self)

        @staticmethod
        def argparse(s):
            try:
                return Action[s.upper()]
            except KeyError:
                return s

    class ProjectAction(argparse.Action):
        '''Store 'project' if not provided
        '''
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            super(ProjectAction, self).__init__(option_strings, dest, **kwargs)
        def __call__(self, parser, namespace, value, option_string=None):
            setattr(namespace, self.dest, value)
            if not namespace.project:
                setattr(namespace, 'project', namespace.branch)

    parser = ArgumentParser(fromfile_prefix_chars='@')
    # Configuration file with command line parameters
    # @NOTE: Any command line switch can be added to override the configuration
    #        if it appears later on the command line
    parser.add_argument('-p', '--pdb',        help='Path to .PDB file')
    parser.add_argument('-P', '--pdbs',       help='Paths to .PDB directories (relative to --build-base)', nargs='*')
    parser.add_argument('-b', '--build-base', help='Build directory path',   default=os.getcwd())
    parser.add_argument('-j', '--project',    help='Repository project (location of cached source)')
    parser.add_argument('-r', '--branch',     help='Remote repository branch', action=ProjectAction, required=True)
    parser.add_argument('-x', '--extensions', help='Semicolon separated list of source extensions (default:cpp;c;h)', default='cpp;c;h')
    parser.add_argument('-s', '--srcsrv',     help='SRCSRV tools directory', default=r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv')
    parser.add_argument('-c', '--scheme',     help='Repository server scheme', default='https://')
    parser.add_argument('-u', '--plugin',     help='Plugin class', default='srcsrv.plugins.Git')
    # Undocumented options
    parser.add_argument('-a', '--action',     help='Action type',            default=Action.INDEX, type=Action.argparse, choices=list(Action))
    # Diagnosis options
    parser.add_argument('-o', '--output',     help='Output file',            default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument('-k', '--keep',       help='Keep temporary artifacts', action='store_true')
    parser.add_argument('-n', '--no-process', help='Donnot change .PDB files', action='store_true')
    parser.add_argument('-l', '--log',        help='Path to log file',       default=None)

    args = parser.parse_args(args=argv)

    indexer.Indexer(args).process()


if __name__ == '__main__':
    main()


