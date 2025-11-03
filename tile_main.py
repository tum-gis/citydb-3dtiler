#External Libraries
import sys

#Internal Libraries
from materializer import *

# Insert the folders to the SYS Environment
sys.path.insert(0, "./classes")
sys.path.insert(0, "./instances")

# Internal Libraries
from sql_blocks import *
from kernel import *

def tile(args):
    query = set_kernel()
    a = create_materilized_view("geometries", str(query))
    print(a)



