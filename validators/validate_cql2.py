import argparse
import sys
import re

def has_unquoted_values(expr):
    #pattern = r"\b\w+\b\s*(=|!=|>|<|>=|<=)\s*([^ ]+)"
    pattern = r"\b\w+\b\s*(=|!=|>|<|>=|<=)\s*([^ ]+)"
    for match in re.finditer(pattern, expr):
        value = match.group(2).strip()
        # If it doesn't start and end with single quotes, it's unquoted
        if not (value.startswith("'") and value.endswith("'")):
            return True

    return False

def has_spatial_operator(expr):
    pattern = r"(s_overlaps|s_within|s_contains|s_crosses|s_disjoint|s_equals|s_intersects|s_touches)"
    if re.match(pattern, expr):
        return True

def has_geometry_types(expr):
    pattern = r"\b(point|multipoint|linestring|multilinestring|polygon|multipolygon|geometrycollection)\s*\(([^)]+)\)"
    return bool(re.search(pattern, expr, re.IGNORECASE))

def fix_geometries(expr):
    pattern = r"\b(point|multipoint|linestring|multilinestring|polygon|multipolygon|geometrycollection)\s*\(([^)]+)\)"
    def replace_geometry(match):
        geom_type = match.group(1)
        content = match.group(2)
        return f"st_geomfromtext('{geom_type}({content})')"
    result = re.sub(pattern, replace_geometry, expr, flags=re.IGNORECASE)
    return result

def add_crs_to_query(expr, epsg_code):
    # Match st_geomfromtext('...') — capture the quoted content
    pattern = r"st_geomfromtext\('([^']+)'\)"

    def add_srid(match):
        geom_text = match.group(1)
        return f"st_geomfromtext('{geom_text}', {epsg_code})"

    result = re.sub(pattern, add_srid, expr)
    return result

def quote_cql2_values(expr):
    pattern = r"(\b\w+\b)\s*(=|!=|>|<|>=|<=|is null|is not null|<>|like|between|in|not like|not in)\s*([^'\s][^ ]*)"

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

    # Check if the geometry referred as ~geom
    if value.find("~geom"):
        value = value.replace("~geom", "gmdt.geometry")

    # Check if it looks like a valid CQL2 expression
    # If it doesn't contain spaces or operators, it's probably missing quotes
    if not any(op in value for op in ['=', '>', '<', 's_intersects', 't_intersects', 's_overlaps', '{', 'op']):
        raise argparse.ArgumentTypeError(
            f"Invalid CQL2 filter: '{value}'\n"
            "Did you forget to wrap the filter in quotes?\n"
            "Correct usage: --filter \"bldg_usage = 'residential'\""
        )
    if has_spatial_operator(value):
        return_val = value
        print("RETURN_VAL", return_val)
    else:
        if has_unquoted_values(value):
            return_val = quote_cql2_values(value)
        else:
            return_val = value
    return return_val
