# Extenral Libraries
import operator
#sorted_x = sorted(x, key=operator.attrgetter('score'))

db_types = ("postgresql", "oracledb")

type_of_effects = ("Ontological", "Spatial", "Semantic", "Temporal", "Visual", "Topological")

class CompositeQueryBlock:
    '''
    A "Combined Query Block" is designed to combine the query blocks in a correct order,
    and the result must be an executable SQL query.
    '''
    def __init__(self, name, db_type, query_blocks):
        self.name = name
        self.db_type = db_type
        self.query_blocks = query_blocks
    def __repr__(self):
        qbs = self.query_blocks
        slct_part = "SELECT"
        frm_part = "FROM"
        join_part = ""
        where_part = ""
        group_part = ""
        for qb in qbs.query_blocks:
            if qb.select_elements != None:
                slct_part += f" {str(qb.select_elements)},"
            else:
                pass
            if qb.from_elements != None:
                frm_part += f" {str(qb.from_elements)},"
            else:
                pass
            if qb.join_elements != None:
                join_part += f" {str(qb.join_elements)}"
            else:
                pass
            if qb.where_elements != None:
                where_part += f" {str(qb.where_elements)}"
            else:
                pass
            if qb.group_elements != None:
                group_part += f" {str(qb.group_elements)}"
            else:
                pass
        slct_part = slct_part[:-1]
        frm_part = frm_part[:-1]

        return f"{slct_part} {frm_part} {join_part} {where_part}"


class QueryBlock:
    '''
    Query Block stores a set of query slices which may defined by a decision by user.
    These "Query Slices" can be bundle of elements used in SELECT-FROM, or in SELECT-JOINs expressions.
    In other words, a regular SQL Query atomized into pieces as fields or subqueries, and
    a query block is a category/bundle of these pieces. It is not a standalone SQL query.
    '''
    def __init__(self, name, type_of_effect, order_number, range_alias=None, description=None, domain_aliases=[], inner_query_blocks=[], select_elements=None, from_elements=None, join_elements=None, where_elements=None, group_elements=None):
        self.name = name
        self.range_alias = range_alias
        self.type_of_effect = type_of_effect
        self.order_number = order_number
        self.domain_aliases = domain_aliases
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
        
        if self.select_elements != None:
            selection_part = f"SELECT {self.select_elements} "
        else:
            selection_part = ""
        if self.from_elements != None:
            from_part = f"FROM {self.from_elements} "
        else:
            from_part = ""
        if self.join_elements != None:
            join_part = f"{self.join_elements} "
        else:
            join_part = ""
        if self.where_elements != None:
            where_part = f"{self.where_elements} "
        else:
            where_part = ""
        if self.group_elements != None:
            group_part = f"{self.group_elements} "
        else:
            group_part = ""
        query = selection_part + from_part + join_part + where_part + group_part
        return query

class QueryBlocks:
    '''
    QueryBlocks is a series of QueryBlock class. It used to store multiple QueryBlock and print the series of SELECT, FROM, JOIN, WHERE statements within the order stored as ORDER_NUMBER.
    '''
    def __init__(self, *query_blocks):
        self.query_blocks = []
        for qb in query_blocks:
            self.query_blocks.append(qb)
    def __repr__(self):
        # First sort the query blocks by using the order_number attribute
        sorted_query_blocks = sorted(self.query_blocks, key=operator.attrgetter('order_number'))
        series_of_query_blocks = ""
        for qb in sorted_query_blocks:
            series_of_query_blocks = series_of_query_blocks + str(qb) + "\n"
        return series_of_query_blocks

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
                if self.range_alias is None:
                    return str(self.field)
                else:
                    return str(self.field+" as "+ self.range_alias)
            elif self.domain_alias is not None:
                if self.range_alias is None:
                    return str(self.domain_alias+"."+self.field)
                else:
                    return str(self.domain_alias+"."+self.field+" as " + self.range_alias)
        elif self.select_type == "case":
            return "case_text"

class SelectElements:
    '''
    SelectElements is a serie of the SelectElement class.
    '''
    def __init__(self, *select_elements, distinct_on = None):
        self.select_elements = []
        self.distinct_on = distinct_on
        for slct in select_elements:
            self.select_elements.append(slct)
    def __repr__(self):
        if self.distinct_on != None:
            selection_part = f"DISTINCT ON ({self.distinct_on}) "
        else:
            selection_part = ""
        for slct in self.select_elements:
            selection_part = selection_part + str(slct) + ", "
        selection_part = selection_part[:-2]
        return selection_part
    def __iter__(self):
        return iter(self.select_elements)
    def __len__(self):
        return len(self.select_elements)
    def __getitem__(self, key):
        return self.select_elements[key]
    

    def add(self, select_element):
        self.select_elements.append(select_element)

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
            if self.alias ==None:
                return f"{str(self.table)} "
            else:
                return str(self.table+" as "+self.alias+" \n")
        elif self.inner_query_blocks is not None:
            for qry in self.inner_query_blocks:
                inners = "("+str(qry)+"),\n"
            inners = inners[:-2]
            return inners

class FromElements:
    '''
    FromElements is a serie of the FromElement class.
    '''
    def __init__(self, *from_elements):
        self.from_elements = []
        for frm in from_elements:
            self.from_elements.append(frm)
    def __repr__(self):
        from_part = ""
        if len(self.from_elements) >= 1:
            for frm in self.from_elements:
                from_part = f"{str(frm)}, "
            from_part = from_part[:-2]
        else:
            from_part = ""
        return from_part

class JoinElement:
    '''
    A JoinElement may have another inner query or a simple join.
    '''
    def __init__(self, join_type, table=None, inner_query_block=None, domain_alias=None, range_alias=None, condition=None):
        self.join_type = join_type
        self.range_alias = range_alias
        self.condition = condition
        if inner_query_block is None:
            self.table = table
            self.domain_alias = domain_alias
            self.inner_query_block = []
        elif table is None:
            self.inner_query_block = inner_query_block
        else: 
            raise ValueError("Join Type can only accept inner query block or table.")
    def __repr__(self):
        if self.inner_query_block == []:
            return f"{str(self.join_type).upper()}  JOIN {self.table} as {self.range_alias} ON {self.condition} "
        elif self.inner_query_block is not None:
            return f"{str(self.join_type).upper()}  JOIN ({str(self.inner_query_block)}) as {self.range_alias} ON {self.condition} "

class JoinElements:
    '''
    FromElements is a serie of the FromElement class.
    '''
    def __init__(self, *join_elements):
        self.join_elements = []
        for jn in join_elements:
            self.join_elements.append(jn)
    def __repr__(self):
        join_part = ""
        for jn in self.join_elements:
            join_part = join_part + str(jn) + "\n"
        return join_part
    def add(self, join_element):
        self.join_elements.append(join_element)

class WhereElement:
    def __init__(self, condition, operator=""):
        self.condition = condition
        self.operator = operator
    def __repr__(self):
        return f"{self.condition} {self.operator}"

class WhereElements:
    def __init__(self, *where_elements):
        self.where_elements = []
        for whr in where_elements:
            self.where_elements.append(whr)
        self.operator = operator
    def __repr__(self):
        where_part = ""
        if len(self.where_elements) >= 1:
            where_part = "WHERE "
            for whr in self.where_elements:
                where_part += f"{str(whr)} "
            where_part = where_part[:-1]
        else:
            where_part = ""
        return where_part

class GroupElement:
        def __init__(self, field):
            self.field = field
        def __repr__(self):
            return f"{self.field}"

class GroupElements:
    def __init__(self, *group_elements):
        self.group_elements = []
        for grp_elm in group_elements:
            self.group_elements.append(grp_elm)
    def __repr__(self):
        group_part = ""
        if len(self.group_elements) >= 1:
            group_part = "GROUP BY "
            for grp_elm in self.group_elements:
                group_part += f"{str(grp_elm)}, "
            group_part = group_part[:-2]
        else:
            group_part = ""
        return group_part