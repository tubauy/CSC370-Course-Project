from current_build import CurrentBuild, SavedBuild
#TODO: error handling (for wrong name input etc)
class Client:
    def __init__(self, connection, username = "Guest"):
        # selections can be converted to int if needed
        self.compoment_selections = {"1": "Motherboards", "2": "CPUs", "3": "RAM", "4": "Storage", "5": "GPUs", "6": "PSUs"}
        self.start_selections = {"1": "Build a PC from scratch", "2": "Edit your existing build"}
        self.component_cache = {}
        self._max_build_name_length = 255

        self.connection = connection
        self.username = username
        self.current_build = None
        self.build_count = 0
        self.build_list = []

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
        #if we exited edit_build_loop, we can save build
        if selection == "1":
            new_build_name = input("Name your build: ")
            while len(new_build_name) <= 0 or len(new_build_name) > self._max_build_name_length:
                print("Name length should be from 1 to 255 characters")
                new_build_name = input("Name your build: ")
            self.current_build = CurrentBuild(self.connection, config_name=new_build_name,user_name = self.username)
            self.edit_build_loop()
            try:
                self.current_build.exit_and_save()
            except ValueError as e:
                print(e)
                print("BUILD WAS NOT SAVED")
            else:
                self.print_build_info()

        elif selection == "2":
            #"Build edit not yet implemented"
            # enter username -> list builds -> pick
            self.print_boilds_of_current_user()
            existing_build_name = self.get_existing_build_input()

            if existing_build_name == None:
                print("Error: Cannot select existing build. Exiting")
                return

            # while len(existing_build_name) <= 0 or len(existing_build_name) > self._max_build_name_length:
            #     print("Name length should be from 1 to 255 characters")
            #     existing_build_name = input("Name of existing build: ")

            try:
                self.current_build = SavedBuild(self.connection, config_name=existing_build_name, user_name=self.username)
            except ValueError as e:
                print(e)
            else:
                self.edit_build_loop()

                #unessecary duplicated code, refactor later?
                try:
                    self.current_build.exit_and_save()
                except ValueError as e:
                    print(e)
                    print("BUILD WAS NOT SAVED")
                else:
                    self.print_build_info()

        print("DONE")

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
            try:
                self.component_cache[component_str] = self.current_build.output_compatible(component_str)
                #   what is the purpose of line 62 and also line 64?
                self.build_component_cache_dict(component_str)
            except ValueError:
                print(f"Already Selected that part. REMOVED {component_str} SELECTION")
                self.current_build.remove_pick(component_str)
                continue

            # print(self.component_cache[component_str])
            self.print_component_selection(component_str)

            selection = input("Select: ")
            if(len(self.component_cache[component_str]) == 0):
                print("NO COMPATIBLE PARTS FOUND")
                continue
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

    def print_boilds_of_current_user(self):
        with self.connection.cursor() as cursor:
            view_name = f"Configurations_{self.username}"
            #cursor.execute(f"SELECT * FROM Configurations WHERE username='{self.username}'")
            cursor.execute(f"SELECT * FROM `{view_name}`")
            builds = cursor.fetchall()
            print("Build names:")

            # reset, print out then add to self's build list and count
            self.build_count = 0
            self.build_list = []
            for build in builds:
                self.build_count += 1
                self.build_list.append(build[0])
                print("   ", build[0])
            self.connection.commit()

    def get_existing_build_input(self):
        if self.build_count == 0:
            print("There is no existing build for this user")
            return None

        existing_build_name = input("Name of existing build?: ")
        while existing_build_name not in self.build_list:
            print("Please enter a build name from the list above")
            existing_build_name = input("Name of existing build?: ")

        return existing_build_name

    def print_build_info(self):
        print("-----------------------")
        print("Final build components:")
        """ for key in self.component_cache.keys():
            cid = self.current_build.picked_items_id[key]
            name = self.component_cache[key][str(cid)]
            print(f"{key}: {name}") """
        print(self.current_build)
        print("BUILD SAVED SUCCESSFULLY")
        print("-----------------------")



