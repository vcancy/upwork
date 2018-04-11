import csv
import re
import os
import sys
import getopt

__author__ = "vcancy"


# /usr/bin/python
# -*-coding:utf-8-*-


class Entry:
    def __init__(self):
        self.last_name = None
        self.fist_name = None
        self.donation = None


class Convertor:
    def __init__(self, input_file, output_file):
        assert os.path.exists(input_file), '{} not exists'.format(input_file)
        self._file_path = input_file
        self._data = None
        self._entrys = list()
        self._out_file = output_file

    def _load(self):
        with open(self._file_path, 'r') as reader:
            self._data = ''.join(reader.readlines())

    def _parse(self):
        datas = [_ for _ in str(self._data).split('\\\'0a') if '$' in _]
        for data in datas:
            if '$' in data:
                _entry = Entry()
                _entry.donation = re.search(r'\$[\d.]+', data).group()
                name_list = data[:data.find('donated') - 1].split(' ')
                if len(name_list) > 2:
                    _entry.fist_name = ' '.join(name_list[:len(name_list) - 1])
                    _entry.last_name = name_list[-1]
                    self._entrys.append(_entry)
                elif len(name_list) == 2:
                    _entry.fist_name = name_list[0]
                    _entry.last_name = name_list[1]
                    self._entrys.append(_entry)
                else:
                    pass

    def _out(self):
        assert self._entrys, 'No lines found in {}'.format(self._file_path)
        with open(self._out_file, 'w') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quoting=csv.QUOTE_MINIMAL)
            spam_writer.writerow(['Fist Name', 'Last Name', 'Donation Amount'])
            for entry in self._entrys:
                spam_writer.writerow([entry.fist_name, entry.last_name, entry.donation])

    def run(self):
        print('start load data from {}'.format(self._file_path))
        self._load()
        print('load data {} characters'.format(len(self._data)))

        print('start parse data')
        self._parse()
        print('found {} count,start output to {}'.format(len(self._entrys), self._out_file))

        self._out()
        print('finish convert')


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('txt2csv.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if not opts:
        print('txt2csv.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('txt2csv.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    convertor = Convertor(inputfile, outputfile)
    convertor.run()


if __name__ == '__main__':
    main(sys.argv[1:])
