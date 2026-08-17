import mysql.connector
#takes a connection object
#returns the username of a user after login
def get_username(connection):
    max_username_length = 255
    username_input = input("ENTER USERNAME: ")
    #check for illegal charecters?
    while(len(username_input) > max_username_length or len(username_input) <= 0):
        print("Please input a valid length username")
        username_input = input("ENTER USERNAME: ")

    username_exists_query = "SELECT 1 FROM `Users` WHERE `username` = %s"
    connection.start_transaction(isolation_level = "SERIALIZABLE")
    try:
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(username_exists_query, (username_input,))
            if(cursor.fetchone() is None):
                print("USERNAME DOES NOT EXIST, CREATING NEW USER")
                create_user_query = (
                    "INSERT INTO `Users` VALUES (%s,%s,NOW())"
                )
                email = f"{username_input}@test.com"
                cursor.execute(create_user_query,(username_input,email)) 
                #add create view here
            else:
                print("USERNAME FOUND")
    except Exception:
        connection.rollback()
        print("ERROR searching Users")
        raise
    else:
        try:
            with connection.cursor(buffered=True) as cursor:
                view_name = f"Configurations_{username_input}"
                                
                create_view_query = (
                    "CREATE OR REPLACE VIEW `%s` AS "
                    "SELECT * FROM `Configurations` WHERE `username` = %s"
                )

                cursor.execute(create_view_query, (view_name, username_input))
        except Exception:
            connection.rollback()
            raise

        else:
            connection.commit()
            return username_input

