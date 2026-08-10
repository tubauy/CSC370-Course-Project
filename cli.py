from current_build import CurrentBuild

class Client:
    def __init__(self, connection):
        # selections can be converted to int if needed
        self.compoment_selections = {"1": "Motherboards", "2": "CPUs", "3": "RAM", "4": "Storage", "5": "GPU", "6": "PSUs"}
        self.start_selections = {"1": "Build a PC from scratch", "2": "Edit your existing build (currently not working)"}
        self.component_cache = {}
        self._max_build_name_length = 255

        self.connection = connection
        self.current_build = None

    def start(self):
        print("-----------------------------")
        print("What do you want to do today?")
        for key, value in self.start_selections.items():
            print(f"{key}) {value}")
        print("-----------------------------")

        selection = input("Select: ")
        while selection not in self.start_selections.keys():
            print("Please select one of the above options")
            selection = input("Select: ")
        
        print(f"You chose to {self.start_selections[selection]}")
        if selection == "1":
            new_build_name = input("Name your build: ")
            while len(new_build_name) <= 0 or len(new_build_name) > self._max_build_name_length:
                print("Name length should be from 1 to 255 characters")
                new_build_name = input("Name your build: ")
            self.current_build = CurrentBuild(self.connection, config_name=new_build_name)
            self.edit_build_loop()
        elif selection == "2":
            "Build edit not yet implemented"
            # enter username -> list builds -> pick
            return

        self.print_build_info()

    def edit_build_loop(self):
        while True:
            print("Select component to choose or edit (or -1 to exit)")
            for key, value in self.compoment_selections.items():
                print(f"{key}: {value}")

            selection = input("Select: ")
            while (selection not in self.compoment_selections.keys() and selection != "-1"):
                print("Please select one of the above options")
                selection = input("Select: ")
            if selection == "-1":
                return

            component_str = self.compoment_selections[selection]

            # store selected component into cache
            self.component_cache[component_str] = self.current_build.output_compatible(component_str)
            self.build_component_cache_dict(component_str)
            # print(self.component_cache[component_str])
            self.print_component_selection(component_str)

            selection = input("Select: ")
            while selection not in self.component_cache[component_str].keys():
                print("Please select one of the above options")
                selection = input("Select: ")

            self.current_build.add_part_test(component_str, int(selection))
            print(f"Selected {component_str} with id {int(selection)}")
            print()

    def print_component_selection(self, component_str):
        for cid, name in self.component_cache[component_str].items():
            print(f"{cid}) {name}")

    def build_component_cache_dict(self, component_str):
        self.component_cache[component_str] = {}
        cur_output = self.current_build.output_compatible(component_str)
        for (cid, name) in cur_output:
            self.component_cache[component_str][str(cid)] = name

    def print_build_info(self):
        print("-----------------------")
        print("Final build components:")
        for key in self.component_cache.keys():
            cid = self.current_build.picked_items_id[key]
            name = self.component_cache[key][str(cid)]
            print(f"{key}: {name}")
        print("-----------------------")



