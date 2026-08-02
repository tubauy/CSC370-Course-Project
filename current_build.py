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
        ("CPU","Motherboards"): (
        "SELECT `component_id` "
        "FROM `Motherboards` "
        "WHERE `Motherboards`.`socket_type` = {cpu_id_socket_type}"),
        ("Motherboards","CPU"): (
        "SELECT `component_id` "
        "FROM `CPU` "
        "WHERE `CPU`.`socket_type` = {motherboard_id_socket_type}"),
        ("CPU","GPU"): (
        "SELECT `component_id` "
        "FROM `GPU` "),
        ("GPU","CPU"): (
        "SELECT `component_id` "
        "FROM `CPU`"),
        ("CPU","RAM"): (
        "SELECT `component_id` "
        "FROM `RAM` "
        "WHERE `RAM`.`ddr_version` = {cpu_id_ddr_version} "
        "AND `RAM`.`capacity_MB` <= {cpu_id_max_ram_capacity}"),
        ("RAM","CPU"): (
        "SELECT `component_id` "
        "FROM `CPU` "
        "WHERE `CPU`.`ddr_version` = {ram_id_ddr_version} "
        "AND `CPU`.`max_ram_capacity_MB` >= {cpu_id_max_ram_capacity} "),
        ("CPU","Storage"): (
        "SELECT `component_id` "
        "FROM `Storage` "),
        ("Storage","CPU"): (
        "SELECT `component_id` "
        "FROM `CPU` "),
        ("Motherboards","GPU"): (
        "SELECT `component_id` "
        "FROM `GPU`"),
        ("GPU","Motherboards"): (
        "SELECT `component_id` "
        "FROM `Motherboards`"),
        ("Motherboards","RAM"): (
        "SELECT `component_id` "
        "FROM `RAM` "
        "WHERE `RAM`.`ddr_version` = {motherboard_id_ddr_version}"),
        ("RAM","Motherboards"): (
        "SELECT `component_id` "
        "FROM `Motherboards` "
        "WHERE `Motherboards`.`ddr_version` = {ram_id_ddr_version} "),
        ("Motherboards","Storage"): (
        "SELECT `component_id` "
        "FROM `Storage`"),
        ("Storage","Motherboards"): (
        "SELECT `component_id` "
        "FROM `Motherboards`"),
        ("GPU","RAM"): (
        "SELECT `component_id` "
        "FROM `RAM`"),
        ("RAM","GPU"): (
        "SELECT `component_id` "
        "FROM `GPU`"),
        ("GPU","Storage"): (
        "SELECT `component_id` "
        "FROM `Storage`"),
        ("Storage","GPU"): (
        "SELECT `component_id` "
        "FROM `GPU`"),
        ("RAM","Storage"): (
        "SELECT `component_id` "
        "FROM `Storage`"),
        ("Storage","RAM"): (
        "SELECT `component_id` "
        "FROM `RAM`")
    }

    def __init__(self, DBconnection):
        #for now, passing connection object instead of cursor
        #allow custom set of parts, i.e add psu or multple storage?
        #values of dict are part id's
        self.picked_items_id = {
            "Motherboard": None,
            "CPU": None,
            "GPU": None,
            "RAM": None,
            "Storage": None
        }

        self.connection = DBconnection
        self.not_yet_picked = ["Motherboard", "CPU", "GPU", "RAM", "Storage"]


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
        result = ""
        if(already_picked):
            return result
        else:
            #run query
            #loop through already picked items and run query for each, based on appropiate condition
            #return list of tuples
            query = ""
            with self.connection.cursor() as cursor:
                pass


    #def addPart(self,type, partId: int):
        #add given part id to the current set
        #check if part of that type already picked
        #check compatability as well
        #if(not self.pickedItemsId[type]):
            


    def exit_and_save(self):
        #save current config to DB and exit
        pass
    
    