def create_materilized_view(name, query):
    mv = '''
    DROP MATERIALIZED VIEW IF EXISTS citydb."
    ''' + name + \
    '''
    ";
    CREATE MATERIALIZED VIEW IF NOT EXISTS citydb."
    ''' + name + \
    '''
    "
    TABLESPACE pg_default
    AS 
    ''' + query + \
    '''
    WITH DATA;
    '''
    return mv

def index_materialized_view(name, geom_column):
    iq = '''
    CREATE INDEX IF NOT EXISTS 
    ''' + name + "_" + geom_column + \
    '''
    _gist ON
    ON 
    ''' + name + \
    '''
     USING gist
    (st_centroid(st_envelope(
    ''' + geom_column + \
    '''
    geom)));
    '''
    return iq