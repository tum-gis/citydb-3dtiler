db_types = ("postgresql", "oracledb")

type_of_effects = ("Ontological", "Spatial", "Semantic", "Temporal", "Visual", "Topological")

class CombinedQueryBlock:
    '''
    A "Combined Query Block" is designed to combine the query blocks in a correct order,
    and the result must be an executable SQL query.
    '''
    def __init__(self, name, db_type, query_blocks):
        self.name = name
        self.com_type = db_type
        self.query_blocks = query_blocks

class QueryBlock:
    '''
    Query Block stores a set of query slices which may defined by a decision by user.
    These "Query Slices" can be bundle of elements used in SELECT-FROM, or in SELECT-JOINs expressions.
    In other words, a regular SQL Query atomized into pieces as fields or subqueries, and
    a query block is a category/bundle of these pieces. It is not a standalone SQL query.
    '''
    def __init__(self, generic_alias, type_of_effect, order_number, aliases, inner_query_blocks=None, select_elements=None, from_elements=None, join_elements=None, where_elements=None, group_elements=None):
        self.generic_alias = generic_alias
        self.type_of_effect = type_of_effect
        self.order_number = order_number
        self.aliases = aliases
        self.inner_query_blocks = inner_query_blocks
        self.select_elements = select_elements
        self.from_elements = from_elements
        self.join_elements = join_elements
        self.where_elements = where_elements
        self.group_elements = group_elements
    def __repr__(self):
        # Change here, it is too primitive
        for e in self.select_elements:
            selection_part+= e + "\n"
        for f in self.from_elements:
            from_part+= f + "\n"
        for j in self.join_elements:
            join_part+= "JOIN" + j + "\n"
        for w in self.where_elements:
            where_part+= w + "\n"
        query = "SELECT \n" + selection_part + "FROM \n" + from_part + join_part + "WHERE \n" + where_part
        return query

