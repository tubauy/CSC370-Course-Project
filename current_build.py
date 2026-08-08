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
        ("CPU","Motherboards"): "ON (`CPU`.`socket_type` = `Motherboards`.`socket_type`)",
        ("Motherboards","CPU"): "ON (`CPU`.`socket_type` = `Motherboards`.`socket_type`)",
        ("CPU","GPU"):"",
        ("GPU","CPU"):"",
        ("CPU","RAM"): "ON (`CPU`.`ddr_version` = `RAM`.`ddr_version` AND `CPU`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
        ("RAM","CPU"): "ON (`CPU`.`ddr_version` = `RAM`.`ddr_version` AND `CPU`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
        ("CPU","Storage"):"",
        ("Storage","CPU"):"",
        ("Motherboards","GPU"):"",
        ("GPU","Motherboards"):"",
        ("Motherboards","RAM"): "ON (`Motherboards`.`ddr_version` = `RAM`.`ddr_version`)",
        ("RAM","Motherboards"): "ON (`Motherboards`.`ddr_version` = `RAM`.`ddr_version`)",
        ("Motherboards","Storage"):"",
        ("Storage","Motherboards"):"",
        ("GPU","RAM"):"",
        ("RAM","GPU"):"",
        ("GPU","Storage"):"",
        ("Storage","GPU"):"",
        ("RAM","Storage"):"",
        ("Storage","RAM"):"",
        ("PSU","CPU"):"",
        ("CPU","PSU"):"",
        ("PSU", "Motherboards"):"",
        ("Motherboards","PSU"):"",
        ("PSU","GPU"):"",
        ("GPU","PSU"):"",
        ("PSU","RAM"):"",
        ("RAM","PSU"):"",
        ("PSU","Storage"):"",
        ("Storage","PSU"):"",
    }

    def __init__(self, DBconnection):
        #Passed connection object, because connection object (not cursor) needed for transaction functions 
        #values of dict are component_id of picked parts
        self.picked_items_id = {
            "Motherboards": None,
            "CPU": None,
            "GPU": None,
            "RAM": None,
            "Storage": None,
            "PSU": None
        }

        self.connection = DBconnection


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
        #using parameterized query for part id's as user can input those
        #TODO: add PSU here
        query = (
            "INSERT INTO `Configurations`(`Motherboard_id`,`CPU_id`,`GPU_id`,`RAM_id`,`Storage_id`) "
            "VALUES (%(Motherboards)s, %(CPU)s, %(GPU)s, %(RAM)s, %(Storage)s)"
        )
        with self.connection.cursor() as cursor:
            cursor.execute(query, self.picked_items_id)
            #TODO: by default doesn't commit, need to add connection.commit statement when function is ready

    
    