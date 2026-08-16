import mysql.connector
#takes a connection object
#returns the username of a user after login
def get_username(connection):
    selection = input("ENTER USERNAME: ")
    username_query = "SELECT 1 FROM `Users` WHERE `username` = %s"
    connection.start_transaction(isolation_level = "SERIALIZABLE")
    try:
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(username_query, selection)
            if(cursor.fetchone() is None):
                print("USERNAME DOES NOT EXIST, CREATING NEW USER")
                #add create view here
            else:
                print("USERNAME FOUND")
    except Exception:
        connection.rollback()
        raise

