# Documents for the Developers

## Development Process (Available Commands and Planned Commands)

<figure style="width:%100;text-align: center;">
  <img src="../images/cli_command_options_and_arguments_design_for_docs.drawio.svg" alt="Usage" style="border:3px solid #005293">
  <figcaption>Using the Application (Semi-transparent sketched boxes indicate features that have not yet been implemented.)</figcaption>
</figure>

## Folders & Files & Classes / Functions

```puml
@startmindmap
!include https://raw.githubusercontent.com/tum-gis/citydb-3dtiler/main/docs/card-style.puml
title Folder & File Structure
right header
<font color=red size=10> Last Check : 22.01.2026</font>
endheader
*[#silver] citydb-3dtiler
**[#silver] <&calculator> io_tools
***[#ghostwhite] <&calculator> folder
****_ create_folder
****_ check_custom_materials
****_ check_file_in
***[#ghostwhite] <&calculator> pg_plpgsql
****_ copy_materials
***[#ghostwhite] <&calculator> pg_sql
****_ read_sql_file
***[#ghostwhite] <&calculator> tiles
****_ generate_tiles
***[#ghostwhite] <&calculator> yaml
****_ read_yaml
****_ write_yaml
**[#silver] <&briefcase> classes
***[#ghostwhite] <&briefcase> advisement
****_ TransformedDict (Abstract)
****_ Advisement
****_ ObjectClass
****_ ObjectClassRecommendations
***[#ghostwhite] <&briefcase> sql_blocks
****_ QueryBlock
****_ QueryBlocks
****_ and_others (see Class Diagram)
**[#silver] <&calculator> database
***[#ghostwhite] <&calculator> pg_connection
****_ pg_show_details
****_ pg_establish
****_ pg_create_session
****_ pg_check_connection
****_ create_materialized_view
****_ index_materialized_view
****_ get_query_results
****_ run_sql
**[#silver] <&droplet> instances
***[#ghostwhite] <&droplet> in_advise
****_ geometry_statistics
****_ recommended_max_features_per_tile
***[#ghostwhite] <&droplet> kernel
****_ krnl_query
***[#ghostwhite] <&droplet> material
****_ objectclass_falldown_addition
****_ properties_falldown_addition
**[#ghostwhite] <&calculator> citydb-3dtiler
**[#ghostwhite] <&calculator> advise_main
**[#ghostwhite] <&calculator> tile_main
**[#ghostwhite] <&calculator> default_paths
legend left
    Icons:
        Main File <&home>
        Functions <&calculator>
        Classes/Dictionaries <&briefcase>
    Box Colors:
        Folders = Gray
        Files = White
endlegend
@endmindmap
```

## Class Diagram of the SQLBlocks Concept

<!--
<figure style="width:%100;text-align: center;">
  <img src="../images/classes.svg" alt="UML Class Diagram" style="border:3px solid #005293">
  <figcaption>UML Class Diagram of the app</figcaption>
</figure>
-->

```puml
@startuml
!include https://raw.githubusercontent.com/tum-gis/citydb-3dtiler/main/docs/card-style.puml
title UML Class Diagram for the SQL-Blocks
header
<font color=red size=10>Last Check : 22.01.2026</font>
endheader
namespace advs <<Advise>> {
  abstract class MutableMapping {
  }
  abstract class TransformedDict {
    store : dict
    ---
    __getitem__()
    __setitem__()
    __delitem__()
    __iter__()
    __len__()
    __repr__()
    _keytransform()
  }
  TransformedDict -up-|> MutableMapping
  class Advisement {
    CommandSet : String
    MaximumFeatures : Integer
    ObjectClasses : List
    ---
    _keytransform()
  }
  Advisement -up-|> TransformedDict
  class ObjectClass {
    name : String
    objectclass_recommendations : Integer
  }
  ObjectClass -up-> TransformedDict
  class ObjectClassRecommendations {
    MaximumFeatures : Integer
  }
  ObjectClassRecommendations -up-|> TransformedDict
}
namespace sqlb <<SQL Blocks>> {
  abstract class AbstractQueryBlock {
    name : String
    range_alias : String
    type_of_effect : TypeOfEffect
    order_number : Integer
    domain_aliases : String[]
    ---
    __repr__()
  }
  AbstractQueryBlock "0..1" o-down-> "1" SelectElements : select_elements
  AbstractQueryBlock "0..1" o-down-> "1" FromElements : from_elements
  AbstractQueryBlock "0..1" o-down-> "1" JoinElements : join_elements
  AbstractQueryBlock "0..1" o-down-> "1" WhereElements : where_elements
  AbstractQueryBlock "0..1" o-down-> "1" GroupElements : group_elements
  class QueryBlock {
  }
  QueryBlock -right-|> AbstractQueryBlock
  class QueryBlocks {
  }
  QueryBlocks -right-|> AbstractQueryBlock
  QueryBlocks *-down-> QueryBlock
  AbstractQueryBlock : inner_query_blocks
  class SelectElement {
    select_type : SelectionType
    field : String
    domain_alias : String
    range_alias : String
    ---
    __repr__()
  }
  SelectElement "*" o-down-> "0..1" CaseWhen : case
  class SelectElements{
    ---
    __repr__()
    __iter__()
    __len__()
    __getitem__()
    add()
  }
  SelectElements *-down-> SelectElement
  class FromElement {
    table : String
    alias : String
    ---
    __repr__()
  }
  FromElement "1" --up-> "*" AbstractQueryBlock : inner_query_blocks
  class FromElements {
    ---
    __repr__()
  }
  FromElements *-down-> FromElement
  class JoinElement {
    type : JoinType
    table : String
    domain_alias : String
    range_alias : String
    condition : String
    ---
    __repr__()
  }
  JoinElement "1" --up-> "*" AbstractQueryBlock : inner_query_block
  class JoinElements {
    ---
    __repr__()
    add()
  }
  JoinElements *-down-> JoinElement 
  class WhereElement {
    condition : String
    operator : Operator
  }
  WhereElement "1" --> WhereElements : inner_where_elements
  class WhereElements {
    ---
    __repr__()
  }
  WhereElements *-down-> WhereElement
  class GroupElement {
    field : String
    ---
    __repr__()
  }
  class GroupElements {
    ---
    __repr__()
  }
  GroupElements *-down-> GroupElement
  class CaseWhen {
    when : String
    then : String
    else: String
  }
  enum DbType {
    postgresql
    oracledb
  }
  enum TypeOfEffect {
    Ontological
    Spatial
    Semantic
    Temporal
    Visual
    Topological
  }
  enum SelectionType {
    field
    case-when
  }
  enum JoinType {
    Left
    Right
    Inner
    Full
  }
}
@enduml
```

## To-Do List

[To-Do List](to-do_list.md){:target="_blank"}


