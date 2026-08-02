#class to track current user config
#passed a mysqlconnector connection object to use
import mysql.connector
class CurrentBuild:
    def __init__(self, DBconnection):
        #for now, passing connection object instead of cursor
        #allow custom set of parts, i.e add psu or multple storage?
        self.picked_items_id = {
            "Motherboard": None,
            "CPU": None,
            "GPU": None,
            "RAM": None,
            "Storage": None
        }


        self.connection = DBconnection


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
        if(already_picked):
            return ""
        else:
            #run query
            #loop through picked_items and run query for each, based on appropiate condition
            pass


    #def addPart(self,type, partId: int):
        #add given part id to the current set
        #check if part of that type already picked
        #check compatability as well
        #if(not self.pickedItemsId[type]):
            


    def exit_and_save(self):
        #save current config to DB and exit
        pass
    
    