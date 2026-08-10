#class to track current user config
#passed a mysqlconnector connection object to use when instantiated
#TODO: make sure inputs are sanitized
import mysql.connector
class CurrentBuild:
    #class variable of ON conditions for JOINS
    #first item in tuple is item already picked, second is relation to be searched
    #empty strings indicate no compatibility constraints, i.e outputs all parts in second category of key pair

    #TODO fill in missing conditions if applicable (MOTHERBOARD, GPU)
    #TODO keep empty strings where no compatability rules exist?
    #TODO account for mirrored tuples (for now hardcoding mirrors)
        # sort key before indexing dict?
    #TODO add indexes in DB to speed joins
    #TODO: change from f strings to parameterized queries, safer
    join_conditions_dict = {
        ("CPUs","Motherboards"): "ON (`CPUs`.`socket_type` = `Motherboards`.`socket_type`)",
        ("Motherboards","CPUs"): "ON (`CPUs`.`socket_type` = `Motherboards`.`socket_type`)",
        ("CPUs","GPUs"):"",
        ("GPUs","CPUs"):"",
        ("CPUs","RAM"): "ON (`CPUs`.`ddr_version` = `RAM`.`ddr_version` AND `CPUs`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
        ("RAM","CPUs"): "ON (`CPUs`.`ddr_version` = `RAM`.`ddr_version` AND `CPUs`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
        ("CPUs","Storage"):"",
        ("Storage","CPUs"):"",
        ("Motherboards","GPUs"):"",
        ("GPUs","Motherboards"):"",
        ("Motherboards","RAM"): "ON (`Motherboards`.`ddr_version` = `RAM`.`ddr_version`)",
        ("RAM","Motherboards"): "ON (`Motherboards`.`ddr_version` = `RAM`.`ddr_version`)",
        ("Motherboards","Storage"):"",
        ("Storage","Motherboards"):"",
        ("GPUs","RAM"):"",
        ("RAM","GPUs"):"",
        ("GPUs","Storage"):"",
        ("Storage","GPUs"):"",
        ("RAM","Storage"):"",
        ("Storage","RAM"):"",
        ("PSUs","CPUs"):"",
        ("CPUs","PSUs"):"",
        ("PSUs", "Motherboards"):"",
        ("Motherboards","PSUs"):"",
        ("PSUs","GPUs"):"",
        ("GPUs","PSUs"):"",
        ("PSUs","RAM"):"",
        ("RAM","PSUs"):"",
        ("PSUs","Storage"):"",
        ("Storage","PSUs"):"",
    }

    def __init__(self, DBconnection, config_name = "Untitled", user_name = "Guest"):
        #Passed connection object, because connection object (not cursor) needed for transaction functions
        #Passed configuration_name for build and username of user making the build 
        #values of dict are component_id of picked parts
        self.picked_items_id = {
            "Motherboards": None,
            "CPUs": None,
            "GPUs": None,
            "RAM": None,
            "Storage": None,
            "PSUs": None
        }

        self.connection = DBconnection
        self.config_name = config_name
        self.user_name = user_name


    def already_picked(self, type):
        #output true/false if already picked part of that type
        if(self.picked_items_id[type] is None):
            return False
        else:
            return True

    def output_compatible(self, type_to_output):
        #output parts in category type_to_output that are compatible with current picks (from picked_items_id)
        #returns parts as list of tuples in form (id, name)

        #builds large JOIN condition, using ON conditions from class variable dict
        #subquerys return parts with specific id using pick_items_id, then those subqueries are aliased and added to JOIN chain
        #TODO: JOIN final result with components table to get names, prices etc
        if(type_to_output not in self.picked_items_id or self.already_picked(type_to_output)):
            return []
        else:
            start_query = f"SELECT `{type_to_output}`.`component_id`, `Components`.`name` FROM `{type_to_output}` JOIN `Components` "
            start_query += f"ON (`{type_to_output}`.`component_id` = `Components`.`component_id`) "

            #get list of items already picked
            current_picked = [k for k, v in self.picked_items_id.items() if v is not None]
            count = 1

            for k in current_picked:
                #get table of parts with that id, all attributes to allow for JOINs to have any ON conditions
                start_query += "JOIN "
                start_query += f"(SELECT * FROM `{k}` WHERE `{k}`.`component_id` = %({k})s) AS p{count} "
                #join this table (holding one specific part) with table of type_to_output
                on_condition = f"{self.join_conditions_dict[(k,type_to_output)]} "
                #string replace function replaces part we already have in ON conditions with appropiate alias
                start_query += on_condition.replace(k, f"p{count}")
                count += 1

            result = None
            try:
                #READ COMMITTED is good enough, because we must check the chosen parts before we insert the build
                #into the configurations table anyway, and there will be a potentially very large gap of time
                #between the user picking parts and saving their build to the database, so parts they have chosen
                #could be deleted from the DB in the interim no matter what isolation level we choose (unless we have 2 hour long transactions!)
                self.connection.start_transaction(isolation_level = "READ COMMITTED")
                with self.connection.cursor() as cursor:
                    cursor.execute(start_query, self.picked_items_id)
                    #using parameters for values of picked_items_id, as those values can be input by user
                    result = list(cursor.fetchall())
            except Exception:
                self.connection.rollback()
                raise
            else:
                self.connection.commit()
                #MUST ALWAYS CLOSE TRANSACTIONS
                return result


    def add_part_test(self,category, partId: int):
        #add given part id to dict of picked items
        #takes category of part being added, and part id of the part
        if(not self.already_picked(category)):
            self.picked_items_id[category] = partId
            #TODO: check if that part is in database? Check with configurations table?
        else:
            pass
            #throw error here?
            


    def exit_and_save(self):
        #save current config to DB Configurations table
        #using parameterized query as we are inserting values that the customer will input

        #TODO: add transaction here 
        #Note: in source code of mysql-connector python, cursor.__exit__ does not handle exceptions, only runs self.close()
        #   so, have to catch exceptions
        query = (
            "INSERT INTO `Configurations`(`configuration_name`,`username`,`motherboard_id`,`ram_id`,`cpu_id`,`storage_id`,`gpu_id`,`psu_id`) "
            "VALUES (%(configuration_name)s, %(username)s, %(Motherboards)s, %(RAM)s, %(CPUs)s, %(Storage)s, %(GPUs)s, %(PSUs)s)"
        )

        #dict of parameters for final insert query
        params_dict = {
            "Motherboards": self.picked_items_id["Motherboards"],
            "CPUs": self.picked_items_id["CPUs"],
            "GPUs": self.picked_items_id["GPUs"],
            "RAM": self.picked_items_id["RAM"],
            "Storage": self.picked_items_id["Storage"],
            "PSUs": self.picked_items_id["PSUs"],
            "configuration_name": self.config_name,
            "username": self.user_name
        }

        try:
            #using repeatble read isolation level, because were are checking if parts user has picked exist in tables
            #before we insert build, and non-repeatable reads could lead to violating constraints
            #However, phantom tuples would only affect transaction if one username is saving two different builds 
            #with the same configuration_name at the same time, is unlikely, and should not be allowed by our user interface anyway
            self.connection.start_transaction(isolation_level = "REPEATABLE READ")
            #using buffered cursor to prevent unfetched results error
            with self.connection.cursor(buffered=True) as cursor:
                #check if user exists
                exists_query = "SELECT 1 FROM `Users` WHERE `username` = %s"
                cursor.execute(exists_query, (self.user_name,))
                if(cursor.fetchone() is None):
                    raise ValueError(f"Unkown User: {self.user_name}")
                    #Should we have seprate class to create users, to be called from CLI?
                
                #check if a user already has a configuration with this name
                #TODO: Ask if user wants to edit current build, or quit without saving (handle from CLI)
                exists_query = "SELECT 1 FROM `Configurations` WHERE (`username` = %s AND `configuration_name` = %s)"
                cursor.execute(exists_query, (self.user_name, self.config_name))
                if(cursor.fetchone() is not None):
                    raise ValueError(f"User: {self.user_name} already has a configuration named {self.config_name}")

                #check if chosen parts exist in category tables
                for k, v in self.picked_items_id.items():
                    if(v is None):
                        continue

                    exists_query = f"SELECT 1 FROM `{k}` WHERE `component_id` = %s"
                    cursor.execute(exists_query, (v,))
                    if(cursor.fetchone() is None):
                        raise ValueError(f"component_id {v} not found in {k} table")
                
                cursor.execute(query, params_dict)
                #NOTE: mysqlconnector automatically replaces None with NULL
                #TODO: by default doesn't commit, need to add connection.commit statement when function is ready
        except Exception:
            self.connection.rollback()
            raise

        else:
            self.connection.commit()
            #self.connection.rollback() #for testing







class SavedBuild(CurrentBuild):
    #loads an existing build from database instead of starting from scratch, and runs UPDATE upon exit_and_save
    def __init__(self, DBconnection, config_name = "Untitled", user_name = "Guest"):
        super().__init__(DBconnection, config_name, user_name)
        #search for existing build in database, if does not exist, error
        try:
            self.connection.start_transaction(isolation_level = "REPEATABLE READ")
            #using buffered cursor to prevent unfetched results errors
            with self.connection.cursor(dictionary=True, buffered=True) as cursor:
                #should also check if user exists?
                exists_query = "SELECT 1 FROM `Configurations` WHERE (`username` = %s AND `configuration_name` = %s)"
                cursor.execute(exists_query, (self.user_name, self.config_name))
                if(cursor.fetchone() is None):
                    raise ValueError(f"User: {self.user_name} does not have a configuration named {self.config_name}")
                #check for multiple returns?
                #Build exists, so load data into picked_items_id
                init_query = (
                    "SELECT `motherboard_id`,`cpu_id`,`gpu_id`,`ram_id`,`storage_id`,`psu_id`"
                    "FROM `Configurations` WHERE `configuration_name` = %s AND `username` = %s"
                )
                cursor.execute(init_query, (self.config_name, self.user_name))
                results_dict = dict(cursor.fetchone())
                #TODO: throw error if dict key doesnt exist (to prevent annoying typo bugs)
                #TODO: clean up with loop
                self.picked_items_id["Motherboards"] = results_dict["motherboard_id"]
                self.picked_items_id["CPUs"] = results_dict["cpu_id"]
                self.picked_items_id["GPUs"] = results_dict["gpu_id"]
                self.picked_items_id["RAM"] = results_dict["ram_id"]
                self.picked_items_id["Storage"] = results_dict["storage_id"]
                self.picked_items_id["PSUs"] = results_dict["psu_id"]

        except Exception:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()

    def test_output(self, category):
        return self.picked_items_id[category]
    
    def exit_and_save(self):
        #this needs to be update instead of insert
        pass
        params_dict = {
                    "Motherboards": self.picked_items_id["Motherboards"],
                    "CPUs": self.picked_items_id["CPUs"],
                    "GPUs": self.picked_items_id["GPUs"],
                    "RAM": self.picked_items_id["RAM"],
                    "Storage": self.picked_items_id["Storage"],
                    "PSUs": self.picked_items_id["PSUs"],
                    "configuration_name": self.config_name,
                    "username": self.user_name
        }
        edit_query = (
            "UPDATE `Configurations` SET "
            "`motherboard_id` = %(Motherboards)s, "
            "`ram_id` = %(RAM)s, "
            "`cpu_id` = %(CPUs)s, "
            "`storage_id` = %(Storage)s, "
            "`gpu_id` = %(GPUs)s, "
            "`psu_id` = %(PSUs)s "
            "WHERE (`configuration_name` = %(configuration_name)s AND `username` = %(username)s)"
        )

        try:
            self.connection.start_transaction(isolation_level = "REPEATABLE READ")
            with self.connection.cursor(buffered=True) as cursor:
                #check if user exists (needed?)
                #exists_query = "SELECT 1 FROM `Users` WHERE `username` = %s"
                #cursor.execute(exists_query, (self.user_name,))
                #if(cursor.fetchone() is None):
                    #raise ValueError(f"Unkown User: {self.user_name}")

                #check if config exists
                exists_query = "SELECT 1 FROM `Configurations` WHERE (`username` = %s AND `configuration_name` = %s)"
                cursor.execute(exists_query, (self.user_name, self.config_name))
                if(cursor.fetchone() is None):
                    raise ValueError(f"User: {self.user_name} does not have a configuration named {self.config_name}")

                #check if chosen parts exist
                for k, v in self.picked_items_id.items():
                    if(v is None):
                        continue

                    exists_query = f"SELECT 1 FROM `{k}` WHERE `component_id` = %s"
                    cursor.execute(exists_query, (v,))
                    if(cursor.fetchone() is None):
                        raise ValueError(f"component_id {v} not found in {k} table")

                cursor.execute(edit_query, params_dict)

        except Exception:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()
            #self.connection.rollback() #for testing

    
    