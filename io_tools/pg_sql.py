#External Libraries
import os

# def read_sql_query(folder, file_name):
def read_sql_file(folder, file_name):
    relative_file_path = os.path.join(folder, file_name)
    try:
        with open(relative_file_path,"r") as advise_query:
            query = advise_query.read()
        return query
    except Error as err:
        print("File reading error:\n {err}")