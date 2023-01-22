import inspect
import os
from itertools import chain
from Bio import SeqIO, Align
# from csv import reader, writer

# from genGroup.settings import MEDIA_ROOT

DEBUG = False
FORMAT = 'fastq'
# OUTPUT_FILE = MEDIA_ROOT + 'processed.' + FORMAT
MEDIA_ROOT = 'C:/Users/S/diplomski/readings/DRB_A'
# MEDIA_ROOT = 'C:/Users/S/diplomski/readings/DQB_A'
# MEDIA_ROOT = 'C:/Users/S/diplomski/readings/temp'


class Filter:
    def __init__(self, filename, format_="fastq"):
        self.readings = []
        self.files = [filename]
        self.format = format

    def cond(self, f):
        self.readings = list(chain.from_iterable(
            [[rec for rec in SeqIO.parse(os.path.join(MEDIA_ROOT, file), FORMAT)
              if f(rec)] for file in self.files]
        ))
        if DEBUG:
            print(f'read {len(self.readings)} sequences')
        return self.readings

    # def try_load_csv(self, f, filtered_length):
    #     try:
    #         with open(self.files[0] + f'{f}.{filtered_length}.filter.csv') as csvfile:
    #             for row in reader(csvfile):
    #                 self.readings.append(row)
    #         if DEBUG:
    #             print(f'successfully read csv with {len(self.readings)} readings')
    #             print(self.readings)
    #         return True
    #     except OSError as err:
    #         if DEBUG:
    #             print(err)
    #             print('Could not open file')
    #         return False
    #
    # def save_csv(self, f, filtered_length):
    #     try:
    #         with open(self.files[0] + f'{f}.{filtered_length}.filter.csv', 'w') as csvfile:
    #             w = writer(csvfile)
    #             for row in self.readings:
    #                 w.writerow(row)
    #         if DEBUG:
    #             print(f'successfully written csv with {len(self.readings)} readings')
    #             print(self.readings)
    #         return True
    #     except OSError as err:
    #         if DEBUG:
    #             print(err)
    #             print('Could not open file')
    #         return False

    def longer_than(self, filtered_length):
        if DEBUG:
            print(f'length longer than {filtered_length}')
        # if self.try_load_csv(current_method_name(), filtered_length):
        #     return self.readings
        # else:
        self.cond(lambda x: len(x.seq) > filtered_length)
        # self.save_csv(current_method_name(), filtered_length)
        return self.readings

    def exact_length(self, filtered_length):
        if DEBUG:
            print(f'length {filtered_length}')
        # if self.try_load_csv(current_method_name(), filtered_length):
        #     print(self.readings)
        #     return self.readings
        # else:
        self.cond(lambda x: len(x.seq) == filtered_length)
        # self.save_csv(current_method_name(), filtered_length)
        # print(len(self.readings))
        # print(self.readings)
        return self.readings

    def length_between(self, filtered_length):
        if DEBUG:
            print(f'min {min(filtered_length) + 1}, max {max(filtered_length) + 1}')
        # if self.try_load_csv(current_method_name(), filtered_length):
        #     return self.readings
        # else:
        self.cond(lambda x: (min(filtered_length) < len(x.seq) < max(filtered_length)))
        # self.save_csv(current_method_name(), filtered_length)
        return self.readings

    # TODO maybe add trimming edges


def current_method_name():
    return inspect.stack()[1].function


if __name__ == '__main__':
    file_ = '099_S99_L001_CS1A-URS_DQB.extendedFrags_filtered.fastq'
    filtered = Filter(file_)
    readings = filtered.exact_length(201)
    print('example seq:')
    print(len(readings))
