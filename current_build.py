#class to track current user config
#passed a mysqlconnector connection object to use
#TODO: make sure inputs are sanitized
import mysql.connector
class CurrentBuild:
    #class variable of WHERE conditions
    #first item in tuple is item already picked, second is relation to be searched
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
        ("Storage","RAM"):""
    }

    def __init__(self, DBconnection):
        #for now, passing connection object instead of cursor
        #allow custom set of parts, i.e add psu or multple storage?
        #values of dict are part id's
        self.picked_items_id = {
            "Motherboards": None,
            "CPU": None,
            "GPU": None,
            "RAM": None,
            "Storage": None
        }

        #always stored picked_items in SQL server to avoid data corruption issues?
        self.connection = DBconnection


    def already_picked(self, type):
        #output true/false if already picked part of that type
        if(self.picked_items_id[type] is None):
            return False
        else:
            return True

    def output_compatible(self, type_to_output):
        #output parts of the chosen type compatible with current build
        #returns list of tuples
        #TODO: account for mirrored tuples
        if(type_to_output not in self.picked_items_id or self.already_picked(type_to_output)):
            return []
        else:
            #run query
            #loop through already picked items and run query for each, based on appropiate condition
            #return list of tuples
            start_query = f"SELECT `{type_to_output}`.`component_id`, `{type_to_output}`.`name` FROM `{type_to_output}` "

            #get list of items already picked
            current_picked = [k for k, v in self.picked_items_id.items() if v is not None]
            with self.connection.cursor() as cursor:
                count = 1
                for k in current_picked:
                    #get table of parts with that id, all attributes
                    start_query += "JOIN "
                    start_query += f"(SELECT * FROM `{k}` WHERE `{k}`.`component_id` = %({k})s) AS p{count} "

                    #join this table (holding one specific part) with table of type_to_output
                    #TODO: allow for insertion of alias into on condition taken from join_conditions_dict (CRITICAL)
                    on_condition = f"{self.join_conditions_dict[(k,type_to_output)]} "
                    start_query += on_condition.replace(k, f"p{count}")
                    count += 1
                #final_query = " ".join(query_commands)
                cursor.execute(start_query, self.picked_items_id)
                result = list(cursor.fetchall())
                return result


    def add_part_test(self,category, partId: int):
        #add given part id to the current set
        #check if part of that type already picked
        #check compatability as well
        #for now, indicate category as well
        if(not self.already_picked(category)):
            self.picked_items_id[category] = partId
            #TODO: check if that part is in database? Check with configurations table?
        else:
            pass
            #throw error here?
            


    def exit_and_save(self):
        #save current config to DB Configurations table and exit
        #destructor method?
        #add transactions, check if id's valid?

        #testing out cursor.execute parameters and implicit concatenation, as per the mysql-conncector dev guide
        query = (
            "INSERT INTO `Configurations`(`Motherboard_id`,`CPU_id`,`GPU_id`,`RAM_id`,`Storage_id`) "
            "VALUES (%(Motherboards)s, %(CPU)s, %(GPU)s, %(RAM)s, %(Storage)s)"
        )
        with self.connection.cursor() as cursor:
            cursor.execute(query, self.picked_items_id)
            #TODO: by default doesn't commit, need to add connection.commit statement when function is ready

    
    