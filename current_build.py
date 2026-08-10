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
        ("CPUs","Motherboards"): "ON (`CPU`.`socket_type` = `Motherboards`.`socket_type`)",
        ("Motherboards","CPUs"): "ON (`CPU`.`socket_type` = `Motherboards`.`socket_type`)",
        ("CPUs","GPUs"):"",
        ("GPUs","CPUs"):"",
        ("CPUs","RAM"): "ON (`CPU`.`ddr_version` = `RAM`.`ddr_version` AND `CPU`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
        ("RAM","CPUs"): "ON (`CPU`.`ddr_version` = `RAM`.`ddr_version` AND `CPU`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
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
        if(type_to_output not in self.picked_items_id or self.already_picked(type_to_output)):
            return []
        else:
            start_query = f"SELECT `{type_to_output}`.`component_id`, `{type_to_output}`.`name` FROM `{type_to_output}` "

            #get list of items already picked
            current_picked = [k for k, v in self.picked_items_id.items() if v is not None]
            with self.connection.cursor() as cursor:
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
                cursor.execute(start_query, self.picked_items_id)
                #using parameters for values of picked_items_id, as those values can be input by user
                result = list(cursor.fetchall())
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

        #TODO: add transaction here - need to test how exceptions are handled using 'with' block for cursor- propogated up?
        query = (
            "INSERT INTO `Configurations`(`configuration_name`,`username`,`Motherboard_id`,`CPU_id`,`GPU_id`,`RAM_id`,`Storage_id`) "
            "VALUES (%(configuration_name)s, %(username)s, %(Motherboards)s, %(CPUs)s, %(GPUs)s, %(RAM)s, %(Storage)s, %(PSUs)s)"
        )
        params_dict = {
            "Motherboards": self.picked_items_id["Motherboards"],
            "CPUs": self.picked_items_id["CPUs"],
            "GPUs": self.picked_items_id["GPUs"],
            "RAM": self.picked_items_id["RAMs"],
            "Storage": self.picked_items_id["Storage"],
            "PSUs": self.picked_items_id["PSUs"],
            "config_name": self.config_name,
            "username": self.user_name
        }
        with self.connection.cursor() as cursor:
            cursor.execute(query, params_dict)
            #TODO: by default doesn't commit, need to add connection.commit statement when function is ready

    
    