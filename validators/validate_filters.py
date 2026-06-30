import argparse
import sys

def validate_cql2(value):
    # Check if it looks like a valid CQL2 expression
    # If it doesn't contain spaces or operators, it's probably missing quotes
    if not any(op in value for op in ['=', 's_intersects', 't_intersects', '{', 'op']):
        raise argparse.ArgumentTypeError(
            f"Invalid CQL2 filter: '{value}'\n"
            "Did you forget to wrap the filter in quotes?\n"
            "Correct usage: --filter \"bldg_usage = '1100'\""
        )
    return value