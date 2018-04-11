import getopt
import os
import csv

import sys

from dcp_parse import pkl_parse, assetmap_parse
from utils.file import shaone_b64
from utils.file import console_progress_bar

__author__ = "vcancy"


# /usr/bin/python
# -*-coding:utf-8-*-

class PklChecker:
    """ PklChecker constructor.
        Args:
            path (str): Absolute path to directory.
        Raises:
            ValueError: ``path`` directory not found.
    """

    def __init__(self, path, output):
        if not os.path.isdir(path):
            raise ValueError("{} is not a valid folder".format(path))
        self._path = path
        self._output = output
        self._pkl = dict()
        self._asset_map = dict()
        self._result = {
            'pass': [],
            'fail': []
        }

    def init_asset_map(self):
        """ Find DCP AssetMap and build Asset List. """
        assetmap_path = os.path.join(self._path, 'ASSETMAP.xml')
        asset_map = assetmap_parse(assetmap_path)['Info']['AssetMap']['AssetList']['Asset']
        for _ in asset_map:
            self._asset_map[_['Id']] = _['ChunkList']['Chunk']['Path']

    def init_pkl(self):
        """ Find DCP PackingList. """
        for _file in os.listdir(self._path):
            if _file.lower().startswith('pkl') and _file.lower().endswith('.xml'):
                asset = os.path.join(self._path, _file)
                pkls = pkl_parse(asset)['Info']['PackingList']['AssetList']['Asset']
                for _ in pkls:
                    self._pkl[_['Id']] = _['Hash']
                break

    def _out(self):
        """ Export check result csv file """
        with open(self._output, 'w') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quoting=csv.QUOTE_MINIMAL)
            spam_writer.writerow(['File', 'Check Status'])
            for status, files in self._result.items():
                for _file in files:
                    sys.stdout.write("{}:{}\n".format(_file, status))
                    spam_writer.writerow([_file, status])
        sys.stdout.write("check result : {}\n".format(self._output))

    def check(self):
        """ Check validity. """
        for _id, _hash in self._pkl.items():
            if _id in self._asset_map:
                _file = self._asset_map[_id]
                path = os.path.join(self._path, _file)
                if _hash == shaone_b64(path, callback=console_progress_bar):
                    self._result['pass'].append(_file)
                else:
                    self._result['fail'].append(_file)

    def run(self):
        """ Process """
        self.init_asset_map()
        self.init_pkl()
        self.check()
        self._out()


def main(argv):
    infile = ''
    outfile = 'out.csv'
    help_describe = '{} -i <dcp path> -o <outfile>'.format(os.path.basename(__file__))
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(help_describe)
        sys.exit(2)
    if not opts:
        print(help_describe)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_describe)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt in ("-o", "--ofile"):
            outfile = arg

    checker = PklChecker(path=infile, output=outfile)
    checker.run()


if __name__ == '__main__':
    main(sys.argv[1:])
