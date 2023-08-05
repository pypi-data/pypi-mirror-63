'''Indexer class
'''
# Python modules
import os
import sys
import git
import pathlib
import argparse
# Source index modules
from . import pdb
from . import base


class Indexer(base.Base):
    '''Source indexer class
    '''
    def __init__(self, args):
        super(Indexer, self).__init__(args)

        # Validate build path
        if not os.path.isdir(args.srcsrv):
            self.logger.error(f'directory {args.srcsrv} does not exist')
            raise FileNotFoundError(f'directory {args.srcsrv} does not exist')
        self.logger.info(args)

        self._sources = None

    @property
    def sources(self):
        '''Create a list of all source files in the repository
        '''
        if self._sources:
            return self._sources

        class SourceDict:
            def __init__(self, args):
                self.sources = {}
                self.args = args

            def __getitem__(self, key):
                try:
                    return self.sources[key]
                except KeyError:
                    class Blob:
                        def __init__(self, args, key):
                            self.path = key[len(args.build_base)-1:].replace('\\', '/')

                    cs_filename = str(pathlib.Path(key).resolve())
                    self.sources.update({ key: Blob(self.args, cs_filename) })
                    return self.sources[key]
        self._sources = SourceDict(self.args)
        return self._sources

    def _index(self):
        ''' Initial indexing during build
        '''
        for bld_dir in self.args.pdbs:
            bld_dir = os.path.join(self.args.build_base, bld_dir)
            if not os.path.isdir(bld_dir):
                self.logger.error('Directory: {bld_dir} not found')
                continue    # Non-fatal error, skip invalid directory

            for dir, subdirs, files in os.walk(bld_dir):
                for fname in files:
                    if fname.endswith('.pdb'):
                        self.args.pdb = os.path.join(dir, fname)
                        pdb.PDB(self).process()

    def _reindex(self):
        ''' @TODO: Process .PDB files after build. This assumes that there's a
                   way to tie back the symbols to the original repo commit hash.
        '''
        pass

    def process(self):
        ''' Process each of the .PDBs
        '''

        if not self.args.pdbs:
            return pdb.PDB(self).process()

        if self.args.action == 1:
            self._index()
        else:
            self._reindex()


__all__ = ['Indexer']
