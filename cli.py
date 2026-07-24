def num_selection(upper_bound, escape='e'):
    """
    gets input as a number and validates it to be at most at upper bound
    used in number selection, returns 'e' for exit, can be given custom
    escape letter.
    """
    selection = input("select:")
    if selection==escape:
        return 'e'
    # check if input is valid
    while not selection.isdigit() or not (0 < int(selection) <= upper_bound):
        selection = input("select:")
    return int(selection)


def get_priority():
    """
    priority message, will run in build from scratch,
    or configurations with more than 1 item missing
    returns alist of component types to be searched in order
    using the algorithm we discussed
    """

    priority_message ="""
    Please select what component is most important to you:
    """
    priorities=[]
    comps_to_pick = ["motherboard", "cpu", "ram", "storage"]

    print(priority_message)
    while len(comps_to_pick)>0:
        print("e: Stop selection.")
        counter = 1
        selection = 0
        for ct in comps_to_pick: # print the option
            print(counter,": ", ct)
            counter+=1

        # get selection until valid number provided
        selection = num_selection(len(comps_to_pick))
        if selection=='e':
            break
        priorities.append(comps_to_pick.pop(selection-1))
    return priorities

def build_from_scratch_option():
    priority_list = get_priority()
    # run the algorithm for the items in the list in order

def search_option():
    search_funcs = []

    print("""
    How to you want to search?
    1: By name.
    2: By type.
    3: By compatibility with other item.
    4: By manufacturer
    """)

    sel = num_selection(4)
    if sel=='e':
        return

    if sel==1:
        print("name:")
        # will call search functions here when they are written
    elif sel==2:
        print("type:")
    elif sel==3:
        print("other item id:")
    elif sel==4:
        print("manufacturer name:")

def find_compat_with_config():
    get_config = [] # replace with the current config
    print("What items are you upgrading?")
    priority_list = get_priority()
    # get items not in the priority list from the config
    # and then search using the algorithm
    

def start():
    # will have the function that will run depending on the selection
    next_op = [build_from_scratch_option, search_option, find_compat_with_config]
    
    print("""
    What do you want to do today?
    1: Build a PC from scratch.
    2: Search items.
    3: Find compatible items to your configuration.
    4: Edit your configuration.
    """)
    selection = num_selection(len(next_op))
    if selection=='e':
        return
    next_op[selection-1]()

    