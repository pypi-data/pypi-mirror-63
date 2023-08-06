""" This is gsnester.py module, and it provides one function called print_nested_lists()
which prints lists that may or may not include nested list
"""
def print_nested_lists(the_list, level):
    """ This function takes two positional argument called 'the_list' and 'level', 'the_list' is
    any Python list(of, possibly, nested lists) and 'level' is used to insert tab-stops when a new list is encountered.
    Each data item in the list is
    (recursively) printed to the screen
    """
    for item in the_list:
            if isinstance(item,list):
                print_nested_lists(item, level+1)
            else:
                for tab_stop in range(level):
                    print("\t", end='')
                print(item)
