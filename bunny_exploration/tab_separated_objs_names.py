"""
Holds function for reading context from tab separated txt file.
Modified version of fca.readwrite.tab_separated by Nikita Romashkin.

Modified in a way to read objects' names from file as well.
"""

import csv
import fca

def read_txt(path):
    """Read context from path, which is tab separated txt file

    Format
    ======

    First line is tab separated attributes' names
    Next an empty line
    The first value in every line is on object name.
    Then tab separated 1 and 0, each line corresponds to one object.

    """
    input_file = open(path, "rb")
    rdr = csv.reader(input_file, delimiter="\t")
    rec = rdr.next()                            # read attributes names

    attributes = []
    for attr in rec:
        attributes.append(str(attr).strip())
    
    rdr.next()                                  # empty line
    
    table = []
    objects = []
    for rec in rdr:
        objects.append(rec[0])                  # read objects names
        line = []
        for num in rec:
            if num == "0":
                line.append(False)
            elif num == "1":
                line.append(True)
        table.append(line)
    input_file.close()

    if len(attributes) != len(table[0]):
        input_file = open(path, "rb")
        attributes = input_file.readline().split("\t")[:-1]
        input_file.close()

    return fca.Context(table, objects, attributes)