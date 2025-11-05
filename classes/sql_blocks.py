db_types = ("postgresql", "oracledb")

type_of_effects = ("Ontological", "Spatial", "Semantic", "Temporal", "Visual", "Topological")

class CombinedQueryBlock:
    '''
    A "Combined Query Block" is designed to combine the query blocks in a correct order,
    and the result must be an executable SQL query.
    '''
    def __init__(self, name, db_type, query_blocks=[]):
        self.name = name
        self.db_type = db_type
        self.query_blocks = query_blocks
    def __repr__(self):
        return str(self.name) + " @" + str(self.db_type) + ':\n' + str(self.query_blocks)

class QueryBlock:
    '''
    Query Block stores a set of query slices which may defined by a decision by user.
    These "Query Slices" can be bundle of elements used in SELECT-FROM, or in SELECT-JOINs expressions.
    In other words, a regular SQL Query atomized into pieces as fields or subqueries, and
    a query block is a category/bundle of these pieces. It is not a standalone SQL query.
    '''
    def __init__(self, name, generic_alias, type_of_effect, order_number, description=None, aliases=[], inner_query_blocks=[], select_elements=[], from_elements=[], join_elements=[], where_elements=[], group_elements=[]):
        self.name = name
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
    # Change this method KingMidas, it is too primitive...
    def __repr__(self):
        # Change here, it is too primitive
        selection_part, from_part, join_part, where_part = ("",)*4
        for idx, e in enumerate(self.select_elements):
            if idx == 0:
                selection_part+= str(e)+"\n"
            else:
                selection_part+= ", "+str(e)+" \n"
        for f in self.from_elements:
            from_part+= str(f)
        for j in self.join_elements:
            join_part+= str(j)
        for w in self.where_elements:
            where_part+= w
        if self.where_elements == []:
            query = "SELECT \n" + selection_part + "FROM " +from_part + join_part
            return query
        elif self.where_elements != []:
            query = "SELECT \n" + selection_part + "FROM " + from_part + join_part + "WHERE " + where_part
            return query

class SelectElement:
    '''
    A SelectElement can be a CASE-WHEN statement or a simple field.
    '''
    def __init__(self, select_type, field=None, case=None, domain_alias=None, range_alias=None):
        self.select_type = select_type
        
        if self.select_type == "field":
            self.field = field
            self.domain_alias = domain_alias
            self.range_alias = range_alias
            self.case = None
        elif self.select_type == "case":
            self.case = case
            self.domain_alias = domain_alias
            self.range_alias = range_alias
            self.field = None
        else:
            raise ValueError("Select Type must be a field or case.")
    def __repr__(self):
        if self.select_type == "field":
            if self.domain_alias is None:
                return str(self.field+" as "+ self.range_alias)
            elif self.domain_alias is not None:
                return str(self.domain_alias+"."+self.field+" as " + self.range_alias)
        elif self.select_type == "case":
            return "case_text"

class JoinElement:
    '''
    A JoinElement may have another inner query or a simple join.
    '''
    def __init__(self, join_type, table=None, inner_query_block=None, domain_alias=None, range_alias=None, condition=None):
        self.join_type = join_type
        if inner_query_block is None:
            self.table = table
            self.domain_alias = domain_alias
            self.range_alias = range_alias
            self.condition = condition
            self.inner_query_block = []
        elif table is None:
            self.inner_query_block = inner_query_block
        else: 
            raise ValueError("Join Type can only accept inner query block or table.")
    def __repr__(self):
        if self.inner_query_block == []:
            if (self.join_type).upper() == "LEFT":
                return str("LEFT JOIN \n"+self.table+" as "+self.range_alias+" ON\n"+self.condition+"\n")
        elif self.inner_query_block is not None:
            return "inner_query_block_text"
class FromElement:
    '''
    A FromElement can have another inner query or a simple table.
    '''
    def __init__(self, table=None, alias=None, inner_query_blocks=[]):
        if inner_query_blocks == []:
            self.table = table
            self.alias = alias
            self.inner_query_blocks = []
        elif table is None:
            self.table = None
            self.alias = None
            self.inner_query_blocks = inner_query_blocks
        else:
            raise ValueError("FromElement can only be a table or a SQL statement reference.")
    def __repr__(self):
        if self.inner_query_blocks == []:
            return str(self.table+" as "+self.alias+" \n")
        elif self.inner_query_blocks is not None:
            return str("inner_query_block_text \n")