#class to track current user config
#passed a mysqlconnector connection object to use
import mysql.connector
class CurrentBuild:
    #class variable of WHERE conditions
    #first item in tuple is item already picked, second is relation to be searched
    #TODO fill in missing conditions if applicable
    #TODO keep empty strings where no compatability rules exist?
    #TODO parse mirrored tuples so they don't have to be included
    join_conditions_dict = {
        ("CPU","Motherboards"): "ON (`CPU`.`socket_type` = `Motherboards`.`Socket_type)",
        ("CPU","GPU"):"",
        ("CPU","RAM"): "ON (`CPU`.`ddr_version` = `RAM`.`ddr_version` AND `CPU`.`max_ram_capacity_MB` >= `RAM`.`capacity_MB`)",
        ("CPU","Storage"):"",
        ("Motherboards","GPU"):"",
        ("Motherboards","RAM"): "ON (`Motherboards`.`ddr_version` = `RAM`.`ddr_version`)",
        ("Motherboards","Storage"):"",
        ("GPU","RAM"):"",
        ("GPU","Storage"):"",
        ("RAM","Storage"):""
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

        self.connection = DBconnection
        self.not_yet_picked = ["Motherboards", "CPU", "GPU", "RAM", "Storage"]


    def test_output(self):
        #test output from DB
        #make cursor
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM `CPU`"
            cursor.execute(query)
            return(list(cursor.fetchall()))



    def already_picked(self, type):
        #output true/false if already picked part of that type
        if(self.picked_items_id["type"] is None):
            return False
        else:
            return True

    def output_compatible(self, type_to_output):
        #output parts of the chosen type compatible with current build
        #gets sanitized input
        #returns list of tuples
        #TODO: account for mirrored tuples
        if(self.already_picked):
            return []
        else:
            #run query
            #loop through already picked items and run query for each, based on appropiate condition
            #return list of tuples
            result = None #for now
            start_query = f"SELECT `{type_to_output}`.`component_id`, `{type_to_output}`.`name` FROM `{type_to_output}` JOIN"

            #get list of items already picked
            current_picked = [k for k, v in self.picked_items_id.items() if v is not None]
            query_commands = []
            query_commands.append(start_query)
            with self.connection.cursor() as cursor:
                count = 1
                for k in current_picked:
                    #get table of parts with that id, all attributes
                    query_commands.append(f"(SELECT * FROM `{k}` WHERE `{k}.`component_id` = {self.picked_items_id[k]}) as p{count}")

                    #join this table (holding one specific part) with table of type_to_output
                    query_commands.append(f"{join_conditions_dict[k,type_to_output]}")
                    count += 1
                final_query = " ".join(query_commands)
                cursor.execute(final_query)
                result = list(cursor.fetchall())
            return result

    #placeholder function for first pickm generalize later
    def first_pick_test(self, category):
        #return list of tuples
        result = None
        with self.connection.cursor() as cursor:
            query = f"SELECT `{category}`.`component_id`,`{category}`.`name` FROM {category}"
            cursor.execute(query)
            result = list(cursor.fetchall())
        return result



    def addPart(self,type, partId: int, category):
        #add given part id to the current set
        #check if part of that type already picked
        #check compatability as well
        #for now, indicate category as well
        if(not self.already_picked(category)):
            picked_items_id[category] = partId
        else:
            pass
            #throw error here?
            


    def exit_and_save(self):
        #save current config to DB and exit
        pass
    
    