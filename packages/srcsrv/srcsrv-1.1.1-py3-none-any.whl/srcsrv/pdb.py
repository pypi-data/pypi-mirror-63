'''Program Database (PDB) parsing and modifying class
'''
# Python modules
import os
import sys
import argparse
import subprocess
# Source index modules
from . import base


class PDB(base.Base):
    '''.PDB processing
    '''
    def __init__(self, si):
        super(PDB, self).__init__(si.args)
        self.path_match = (self.args.build_base + '*.').replace('\\', '\\\\')
        self.si = si
        self._sources = None
 
    @property
    def sources(self):
        '''Property containing a list of source files in the current source tree
        :return List of source files
        '''
        if self._sources:
            return self._sources

        srctool = os.path.join(self.args.srcsrv, 'srctool.exe')
        self.args.pdb = os.path.join(self.args.build_base, self.args.pdb)
        files = []
        try:
            for ext in self.args.extensions.split(';'):
                cp = subprocess.run([srctool, '-r', '-z', '-h', f'-l:{self.path_match}' + ext, self.args.pdb], stdout=subprocess.PIPE, check=True)
                files = files + cp.stdout.splitlines()[:-1]
        except subprocess.CalledProcessError:
            self.logger.error(f'{srctool} returned an error processing {self.args.pdb}')
            self._sources = {}
            return self._sources

        # create dict of MD5 values keyed on the file name
        files_list = [file.decode().split('\t Checksum MD5: ') for file in files]
        self._sources = dict(files_list)
        if len(self._sources):
            self.logger.info(f'{self.args.pdb} contains: {self._sources}')

            # Now that we know that there's files we can open matching .ini
            self.args.output = argparse.FileType('w')(self.args.pdb[:-4] + '.ini')
        else:
            self.logger.warning(f'{self.args.pdb} no source files found')
            self._sources = {}
        
        return self._sources

    def process(self):
        ''' Process a single .PDB
        '''
        if len(self.sources) == 0:
            self.logger.info(f'{self.args.pdb} has no source files')
            return

        self.args.output.write(f'''SRCSRV: ini ------------------------------------------------
VERSION=2
VERCTRL=
SRCSRV: variables ------------------------------------------
BUILD_BASE={self.args.build_base}
''')

        # Write VARIABLES section of SRCSRV.ini
        self.args.plugin.process()
        self.args.output.write('''SRCSRV: source files ---------------------------------------
''')

        for src, md5 in self.sources.items():
            try:
                # find matching repository file
                code = self.si.sources[src]
            except KeyError:
                self.logger.warning(f'Could not found {src} in {self.args.pdb}')
                continue
            # Write source file item to SRCSRV.ini
            self.args.plugin.process(src, code, md5)

        self.args.output.write('''SRCSRV: end ------------------------------------------------''')

        if self.args.output != sys.stdout:
            # Write the the output file onto the .PDB
            self.args.output.close()
            if not self.args.no_process:
                pdbstr = os.path.join(self.args.srcsrv, 'pdbstr.exe')
                try:
                    cp = subprocess.run([pdbstr, '-w', f'-p:{self.args.pdb}', f'-s:srcsrv', f'-i:{self.args.output.name}'], check=True)
                except subprocess.CalledProcessError:
                    self.logger.error(f'{pdbstr} returned an error processing {self.args.pdb}')

            if not self.args.keep:
                # Remove the output file
                os.remove(self.args.output.name)


__all__ = ['PDB']

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pdb',        help='Path to .PDB file')
    parser.add_argument('-b', '--build-base', help='Build directory path')
    parser.add_argument('-s', '--srcsrv',     help='SRCSRV tools directory',  default=r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv')
    pdb = PDB(parser.parse_args())
    print(pdb.sources)
