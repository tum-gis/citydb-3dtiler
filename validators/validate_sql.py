import argparse
import sys
import re

def has_unquoted_values(expr: str) -> bool:
    pattern = r"\b\w+\b\s*(=|!=|>=|<=|>|<)\s*('[^']*'|[^'\s]+)"

    for match in re.finditer(pattern, expr):
        value = match.group(2)

        # if not properly quoted → it's invalid
        if not (value.startswith("'") and value.endswith("'")):
            return True

    return False

def quote_sql_values(expr: str) -> str:
    # (\b\w+\b) : Column name
    # (=|!=|>=|<=|>|<) : Comparisons Operators
    # ('.*?'|\d+(?:\.\d+)?|\w+) : String, integer or floats
    pattern = r"(\b\w+\b)\s*(=|!=|>=|<=|>|<)\s*('.*?'|\d+(?:\.\d+)?|\w+)"

    def replacer(match):
        field = match.group(1)
        op = match.group(2)
        value = match.group(3)

        # already quoted → leave as-is
        if value.startswith("'") and value.endswith("'"):
            return match.group(0)

        return f"{field} {op} '{value}'"

    return re.sub(pattern, replacer, expr)

def validate_sql(value):
    # Check if the geometry referred as ~geom
    if value.find("~geom"):
        new_value = value.replace("~geom", "gmdt.geometry")

    # Check if it looks like a valid CQL2 expression
    # If it doesn't contain spaces or operators, it's probably missing quotes
    if not any(op in value for op in ['=', '>', '<', 'st_intersect', 'st_intersects', '&&', '@', 'st_contains', 'st_dwithin']):
        raise argparse.ArgumentTypeError(
            f"Invalid SQL filter: '{value}'\n"
            "Did you forget to wrap the filter in quotes?\n"
            "Correct usage: --sql-filter \"bldg_usage = 'residential'\""
        )

    if has_unquoted_values(new_value):
        # print("has unquoted values!!!")
        return_val = quote_sql_values(new_value)
        print(return_val)
    else:
        # print("all values are quoted.")
        return_val = new_value

    return return_val
