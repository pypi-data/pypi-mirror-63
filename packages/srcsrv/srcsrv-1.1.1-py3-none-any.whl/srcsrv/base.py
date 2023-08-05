'''Program Database (PDB) parsing base class
'''
# Python modules
import logging


class Base(object):
    '''Base class for source indexing
    '''
    def __init__(self, args):
        self.args = args
        # Make sure the path ends with '\\'
        if not self.args.build_base.endswith('\\'):
            self.args.build_base = args.build_base + '\\'

        logging.basicConfig(filename=self.args.log, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('Source_Indexing')


__all__ = ['Base']
