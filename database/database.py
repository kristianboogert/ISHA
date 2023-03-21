from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host = "localhost",
        user = input("Enter username: "),
        password = getpass("Enter password: "),
        database = "testdatabase",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")

        # create_user_type = """
        #     CREATE TABLE user_type(
        #         id INT AUTO_INCREMENT PRIMARY KEY,
        #         user_name VARCHAR(100),
                
        # )
        # """
    print(connection)
    # with connection.cursor() as cursor:
    #     cursor.execute(create_user_type)
    #     connection.commit()

except Error as err:
    print(err)