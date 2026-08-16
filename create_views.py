def create_view(username):

    view_name = f"configurations_{username}"

    sql = (
        f"CREATE OR REPLACE VIEW `{view_name}` AS\n"
        f"SELECT * FROM `Configurations` WHERE `username` = {username}"
    )