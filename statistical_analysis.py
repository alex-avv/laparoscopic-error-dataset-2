''' Used to perform statistical analysis of OCHRA information.

Paste the event's information (as printed from the utils.info_label or utils.
info_error functions) into the event_info array.
'''
import numpy as np
import re

event_info = np.array(['A', 'K', 'L', 'C', 'K', 'A', 'B', 'B', 'B', 'C', 'L', 'E', 'G', 'P', 'G', 'M', 'G', 'E', 'A', 'G', 'K', 'P', 'G', 'K', 'Q', 'A', 'C', 'H', 'K', 'L', 'I', 'G', 'G', 'L', 'G', 'B', 'F', 'P', 'H', 'K', 'G', 'Q', 'G', 'Q', 'Q', 'B', 'K', 'C', 'K', 'P', 'P', 'C', 'G', 'J', 'C', 'K', 'F', 'G', 'C', 'L', 'P', 'K', 'B', 'Q', 'G', 'F', 'A', 'C', 'C', 'C', 'G', 'B', 'G', 'G', 'G', 'K', 'G', 'L', 'G', 'G', 'B', 'F', 'L', 'K', 'M', 'L', 'K', 'K', 'E', 'I', 'P', 'K', 'I', 'G', 'P', 'C', 'G', 'L', 'K', 'L', 'K', 'A', 'G', 'G', 'A', 'A', 'A', 'P', 'P', 'L', 'B', 'G', 'G', 'M', 'E', 'F', 'B', 'C', 'C', 'F', 'M', 'F', 'M', 'C', 'B', 'N', 'Q', 'G', 'M', 'G', 'J', 'G', 'G', 'H', 'K', 'B', 'H', 'G', 'L', 'G', 'A', 'E', 'B', 'L', 'H', 'J', 'G', 'C', 'M', 'F', 'K', 'C', 'D', 'C', 'K', 'C', 'M', 'M', 'A', 'A', 'K', 'E', 'D', 'B', 'K', 'C', 'P', 'E', 'P', 'L', 'C', 'C', 'B', 'J', 'G', 'M', 'F', 'K', 'B', 'F', 'K', 'N', 'K', 'I', 'K', 'E', 'D', 'K', 'P', 'A', 'L', 'E', 'H', 'N', 'G', 'B', 'M', 'G', 'N', 'B', 'B', 'C', 'B', 'J', 'G', 'G', 'G', 'G', 'G', 'N', 'M', 'M', 'L', 'K', 'B', 'C', 'L', 'L', 'K', 'K', 'K', 'H', 'L', 'L', 'P', 'J', 'I', 'C', 'P', 'F', 'I', 'E', 'L', 'G', 'B', 'C', 'C', 'G', 'K', 'F', 'G', 'G', 'L', 'H', 'K', 'N', 'K', 'P', 'G', 'D', 'K', 'M', 'I', 'B', 'C', 'L', 'C', 'P', 'D', 'C', 'G', 'A', 'G', 'J', 'K', 'L', 'A', 'K', 'N', 'L', 'K', 'P', 'B', 'L', 'I', 'L', 'G', 'B', 'A', 'P', 'E', 'H', 'K', 'M', 'K', 'A', 'B', 'K', 'C', 'L', 'G', 'J', 'J', 'B', 'C', 'P', 'P', 'A', 'E', 'A', 'I', 'J', 'A', 'G', 'J', 'C', 'K', 'A', 'L', 'O', 'Q', 'C', 'J', 'G', 'G', 'L', 'K', 'G', 'B', 'B', 'B', 'M', 'J', 'C', 'P', 'A', 'C', 'G', 'F', 'A', 'G', 'B', 'G', 'F', 'K', 'E', 'L', 'P', 'K', 'A', 'A', 'Q', 'K', 'G', 'P', 'K', 'L', 'C', 'G', 'F', 'K', 'L', 'N', 'G', 'G', 'H', 'E', 'K', 'A', 'A', 'G', 'P', 'C', 'C', 'J', 'N', 'K', 'P', 'I', 'P', 'P', 'K', 'N', 'C', 'B', 'E', 'P', 'B', 'E', 'O', 'C', 'P', 'C', 'D', 'C', 'G', 'M', 'C', 'P', 'G', 'K', 'K', 'C', 'C', 'L', 'H', 'K', 'J', 'K', 'K', 'E', 'A', 'E', 'G', 'G', 'B', 'G', 'G', 'P', 'G', 'B', 'K', 'K', 'H', 'K', 'G', 'J', 'K', 'D', 'F', 'M', 'C', 'D', 'G', 'B', 'K', 'G', 'M', 'I', 'K', 'F', 'E', 'I', 'A', 'G', 'P', 'I', 'C', 'A', 'J', 'C', 'K', 'G', 'C', 'C', 'G', 'A', 'J', 'G', 'B', 'J', 'B', 'B', 'B', 'M', 'H', 'G', 'D', 'L', 'G', 'B', 'E', 'H', 'G', 'E', 'F', 'B', 'G', 'A', 'H', 'L', 'E', 'G', 'G', 'C', 'G', 'G', 'Q', 'G', 'E', 'M', 'K', 'G', 'G', 'E', 'B', 'J', 'P', 'K', 'G', 'C', 'C', 'G', 'L', 'B', 'B', 'P', 'K', 'E', 'J', 'C', 'E', 'E', 'G', 'B', 'C', 'C', 'K', 'G', 'K', 'G', 'E', 'F', 'G', 'E', 'G', 'L', 'P', 'K', 'G', 'K', 'K', 'G', 'L', 'C', 'G', 'A', 'A', 'G', 'C', 'K', 'G', 'G', 'B', 'E', 'G', 'L', 'G', 'K', 'I', 'P', 'B', 'A', 'K', 'F', 'K', 'D', 'C', 'H', 'J', 'P', 'K', 'E', 'N', 'P', 'G', 'G', 'G', 'G', 'F', 'E', 'G', 'E', 'E', 'A', 'L', 'B', 'G', 'G', 'G', 'P', 'J', 'G', 'B', 'G', 'G', 'L', 'E', 'K', 'G', 'L', 'C', 'K', 'J', 'G', 'G', 'J', 'F', 'K', 'J', 'K', 'P', 'E', 'N', 'D', 'E', 'L', 'F', 'G', 'L', 'A', 'P', 'K', 'I', 'P', 'L', 'G', 'F', 'P', 'E', 'G', 'G', 'A', 'C', 'B', 'G', 'B', 'F', 'F', 'P', 'E', 'P', 'G', 'G', 'H', 'F', 'G', 'G', 'E', 'L', 'F', 'K', 'K', 'K', 'A', 'L', 'B', 'A', 'J', 'G', 'A', 'C', 'L', 'K', 'E', 'J', 'P', 'C', 'L', 'K', 'H', 'Q', 'H', 'A', 'E', 'G', 'G', 'G', 'C', 'L', 'K', 'G', 'G', 'E', 'E', 'H', 'F', 'J', 'Q', 'I', 'J', 'B', 'A', 'P', 'G', 'L', 'A', 'M', 'A', 'G', 'H', 'E', 'A', 'C', 'A', 'G', 'E', 'B', 'J', 'L', 'G', 'B', 'E', 'H', 'G', 'M', 'L', 'G', 'G', 'K', 'D', 'A', 'N', 'A', 'A', 'C', 'A', 'B', 'P', 'E', 'C', 'K', 'M', 'K', 'G', 'A', 'G', 'G', 'Q', 'G', 'A', 'G', 'A', 'Q', 'G', 'G', 'J', 'J', 'A', 'P', 'G', 'D', 'D', 'E', 'D', 'P', 'B', 'B', 'H', 'P', 'M', 'H', 'G', 'E', 'L', 'N', 'G', 'C', 'F', 'B', 'K', 'B', 'J', 'A', 'N', 'M', 'L', 'J', 'C', 'H', 'E', 'G', 'C', 'H', 'K', 'F', 'K', 'G', 'B', 'M', 'E', 'K', 'K', 'G', 'K', 'G', 'K', 'F', 'G', 'F', 'G', 'F', 'L', 'F', 'P', 'J', 'D', 'M', 'K', 'E', 'K', 'K', 'E', 'B', 'L', 'E', 'G', 'I', 'J', 'E', 'B', 'M', 'J', 'J', 'G', 'B', 'P', 'L', 'I', 'M', 'P', 'G', 'A', 'J', 'G', 'J', 'A', 'B', 'B', 'I', 'B', 'D', 'D', 'P', 'P', 'L', 'P', 'G', 'P', 'P', 'P', 'B', 'F', 'Q', 'C', 'L', 'P', 'K', 'L', 'P', 'J', 'L', 'G', 'K', 'E', 'B', 'E', 'J', 'G', 'B', 'L', 'L', 'G', 'I', 'G', 'J', 'L', 'A', 'H', 'L', 'G', 'G', 'K', 'M', 'L', 'C', 'G', 'C', 'L', 'L', 'G', 'G', 'K', 'K', 'K', 'H', 'K', 'L', 'P', 'L', 'O', 'L', 'K', 'L', 'G', 'J', 'L', 'P', 'F', 'G', 'K', 'D', 'G', 'L', 'G', 'B', 'I', 'G', 'E', 'G', 'I', 'M', 'I', 'P', 'K', 'B', 'E', 'B', 'G', 'G', 'P', 'F', 'G', 'C', 'F', 'K', 'B', 'C', 'P', 'G', 'D', 'H', 'B', 'K', 'L', 'G', 'J', 'N', 'E', 'C', 'B', 'G', 'K', 'C', 'I', 'B', 'A', 'E', 'Q', 'L', 'G', 'E', 'H', 'G', 'G', 'E', 'K', 'G', 'G', 'G', 'L', 'B', 'K', 'A', 'B', 'P', 'B', 'K', 'N', 'L', 'B', 'Q', 'Q', 'G', 'N', 'P', 'C', 'F', 'F', 'K', 'C', 'F', 'L', 'E', 'B', 'Q', 'D', 'K', 'Q', 'N', 'F', 'G', 'C', 'G', 'G', 'C', 'G', 'H', 'G', 'G', 'K', 'K', 'G', 'L', 'H', 'G', 'A', 'G', 'B', 'H', 'G', 'L', 'C', 'D', 'A', 'E', 'B', 'C', 'M', 'L', 'G', 'O', 'H', 'G', 'L', 'B', 'K', 'G', 'G', 'J', 'K', 'K', 'G', 'L', 'A', 'E', 'E', 'K', 'C', 'C', 'I', 'E', 'B', 'C', 'G', 'G', 'K', 'G', 'L', 'J', 'B', 'J', 'G', 'G', 'K', 'G', 'A', 'C', 'J', 'P', 'K', 'B', 'L', 'C', 'L', 'L', 'G', 'A', 'G', 'K', 'M', 'C', 'H', 'K', 'P', 'G', 'N', 'L', 'G', 'G', 'G', 'A', 'M', 'K', 'E', 'G', 'A', 'G', 'L', 'I', 'G', 'L', 'P', 'A', 'G', 'K', 'B', 'E', 'E', 'P', 'B', 'G', 'K', 'F', 'C', 'A', 'G', 'A', 'P', 'D', 'A', 'K', 'B', 'L', 'J', 'B', 'L', 'E', 'E', 'G', 'G', 'F', 'G', 'D', 'O', 'G', 'G', 'G', 'B', 'A', 'L', 'L', 'D', 'E', 'B', 'G', 'G', 'L', 'G', 'G', 'H', 'K', 'P', 'P', 'A', 'G', 'L', 'J', 'P', 'A', 'B', 'G', 'K', 'P', 'D', 'H', 'G', 'C', 'I', 'K', 'A', 'K', 'G', 'E', 'A', 'F', 'E', 'G', 'G', 'G', 'K', 'P', 'B', 'A', 'G', 'F', 'E', 'G', 'F', 'P', 'C', 'I', 'K', 'P', 'A', 'G', 'Q', 'F', 'C', 'G', 'M', 'C', 'C', 'O', 'G', 'H', 'G', 'L', 'L', 'E', 'E', 'C', 'B', 'A', 'B', 'C', 'K', 'K', 'N', 'J', 'F', 'A', 'G', 'L', 'B', 'G', 'E', 'A', 'N', 'G', 'K', 'M', 'A', 'D', 'K', 'G', 'D', 'G', 'I', 'B', 'E', 'F', 'D', 'J', 'F', 'N', 'B', 'C', 'N', 'F', 'G', 'G', 'K', 'F', 'A', 'L', 'K', 'K', 'P', 'K', 'J', 'G', 'J', 'B', 'F', 'G', 'N', 'B', 'P', 'C', 'G', 'G', 'J', 'G', 'P', 'L', 'J', 'E', 'E', 'F', 'F', 'G', 'E', 'K', 'L', 'G', 'G', 'F', 'P', 'F', 'K', 'L', 'P', 'A', 'B', 'K', 'A', 'L', 'P', 'H', 'K', 'C', 'P', 'C', 'C', 'G', 'G', 'H', 'E', 'F', 'K', 'G', 'C', 'J', 'N', 'E', 'I', 'B', 'E', 'C', 'K', 'I', 'N', 'K', 'N', 'C', 'G', 'K', 'K'
                       ])
event_info_no_repeat = list(set(event_info))


def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect.

    Code from https://stackoverflow.com/questions/2669059/how-to-sort-alpha-
    numeric-set-in-python.
    """
    def convert(text): return int(text) if text.isdigit() else text

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


# Sorting in alphanumerical order
event_info_no_repeat = sorted_nicely(event_info_no_repeat)

# Printing the results
for event_name in event_info_no_repeat:
    counter = 0
    for event_instance in event_info:
        if event_instance == event_name:
            counter += 1
    # print(f'{event_name} phases: {counter} cases')  # Uncomment if 'total'
    # flag is enabled
    print(f'{event_name}: {counter} cases')  # Comment if 'total' flag is
    # enabled
