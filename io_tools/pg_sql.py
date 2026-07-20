#External Libraries
import os
import re

# def read_sql_query(folder, file_name):
def read_sql_file(folder, file_name):
    relative_file_path = os.path.join(folder, file_name)
    try:
        with open(relative_file_path,"r") as advise_query:
            query = advise_query.read()
            return query, relative_file_path
    except Error as err:
        print("File reading error:\n {err}")

def append_pro_value(expr):
    pattern = r"(\b\w+\b)(\s*(?:=|!=|>|<|>=|<=)\s*(?:'[^']*'|\S+))"

    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}.pro_value{m.group(2)}",
        expr
    )