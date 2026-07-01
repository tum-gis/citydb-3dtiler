import argparse
import sys
import re

def has_unquoted_values(expr):
    pattern = r"\b\w+\b\s*(=|!=|>|<|>=|<=)\s*([^ ]+)"

    for match in re.finditer(pattern, expr):
        value = match.group(2).strip()

        # If it doesn't start and end with single quotes, it's unquoted
        if not (value.startswith("'") and value.endswith("'")):
            return True

    return False

def quote_cql2_values(expr):
    pattern = r"(\b\w+\b)\s*(=|!=|>|<|>=|<=)\s*([^'\s][^ ]*)"

    def replacer(match):
        field = match.group(1)
        operator = match.group(2)
        value = match.group(3)

        # Skip if already quoted
        if value.startswith("'") and value.endswith("'"):
            return match.group(0)

        return f"{field} {operator} '{value}'"

    # print(f"(i) Info : CQL2 filter changed as : {re.sub(pattern, replacer, expr)}")
    return re.sub(pattern, replacer, expr)

def validate_cql2(value):
    # Check if it looks like a valid CQL2 expression
    # If it doesn't contain spaces or operators, it's probably missing quotes
    if not any(op in value for op in ['=', '>', '<', 's_intersects', 't_intersects', '{', 'op']):
        raise argparse.ArgumentTypeError(
            f"Invalid CQL2 filter: '{value}'\n"
            "Did you forget to wrap the filter in quotes?\n"
            "Correct usage: --filter \"bldg_usage = 'residential'\""
        )

    if has_unquoted_values(value):
        return_val = quote_cql2_values(value)
    else:
        return_val = value

    return return_val
