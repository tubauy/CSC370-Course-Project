from current_build import CurrentBuild

class Client:
    def __init__(self, connection):
        # selections can be converted to int if needed
        self.selections = {"1": "Build a PC from scratch", "2": "Edit your configuration"}
        self.connection = connection
        self.current_build = None

    def start(self):
        print("-----------------------------")
        print("What do you want to do today?")
        for keys in self.selections:
            print(f"{keys}: {self.selections[keys]}")
        print("-----------------------------")

        selection = input("Select: ")
        while selection not in self.selections.keys():
            print("Please select one of the above options")
            selection = input("Select: ")
        
        print(f"You chose to {self.selections[selection]}")
        if selection == "1":
            self.current_build = CurrentBuild(self.connection)
        elif selection == "2":
            config_name = input("What do you like to name your Build: ")
            self.current_build = CurrentBuild(self.connection, config_name=config_name)

        print(self.current_build.output_compatible("Motherboards"))


# def get_priority():
#     """
#     priority message, will run in build from scratch,
#     or configurations with more than 1 item missing
#     returns alist of component types to be searched in order
#     using the algorithm we discussed
#     """
#
#     priority_message ="""
#     Please select what component is most important to you:
#     """
#     priorities=[]
#     # added new parts here for testing, file not complete, not ready yet
#     comps_to_pick = ["Motherboard", "CPU", "GPU", "RAM", "storage"]
#
#     print(priority_message)
#     while len(comps_to_pick)>0:
#         print("e: Stop selection.")
#         counter = 1
#         selection = 0
#         for ct in comps_to_pick: # print the option
#             print(counter,": ", ct)
#             counter+=1
#
#         # get selection until valid number provided
#         selection = num_selection(len(comps_to_pick))
#         if selection=='e':
#             break
#         priorities.append(comps_to_pick.pop(selection-1))
#     return priorities
