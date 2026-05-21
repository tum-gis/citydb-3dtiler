# Test Procedures

## Test Procedures Diagram

```puml
@startmindmap
title Test Procedure of citydb-3dtiler application
header
<font color=indianred size=12><b>Last Check : 20.05.2026</b></font>
<font color=indianred size=12><b>Expected Release : 0.9.3</b></font>
endheader

'!include card-style.puml

* Tests

**: Single Tileset
<font color=gray><i>tile</i></font>
;
***: Custom Color Set 
<font color=gray><i>tile --custom-style tum_colors.csv</i></font>
;
***: Property-based Color Set
<font color=gray><i>tile --style-mode property-based</i></font>
;
***: Transparency Mode
<font color=gray><i>tile --transparency blend</i></font>
;
***: To a Custom Folder
<font color=gray><i>tile --output-folder</i></font>
;
***: No Style Mode
<font color=gray><i>tile --style-mode no-style</i></font>
;
**: For Separate Tilesets (objectclass)
<font color=gray><i>--separate-tilesets objectclass \ </i></font>
<font color=gray><i>tile</i></font>
;
***: Property-based Color Set
<font color=gray><i>--separate-tilesets objectclass \ </i></font>
<font color=gray><i>tile \ </i></font>
<font color=gray><i>--style-mode property-based</i></font>
;
****: Selected Attributes in tabular format
<font color=gray><i>--separate-tilesets objectclass \ </i></font>
<font color=gray><i>tile \ </i></font>
<font color=gray><i> --style-mode property-based \ </i></font>
<font color=gray><i>--attributes selected \ </i></font>
<font color=gray><i>--selected-attributes  core_name,gen_objektart</i></font>
;
****: Selected Attributes in nested/json format
<font color=gray><i>--separate-tilesets objectclass \ </i></font>
<font color=gray><i>tile \ </i></font>
<font color=gray><i>--style-mode property-based \ </i></font>
<font color=gray><i>--attributes selected \ </i></font>
<font color=gray><i>--attribute-structure nested \ </i></font>
<font color=gray><i>--selected-attributes core_name,gen_objektart,con_height</i></font>
;
****: All Attributes in nested/json format
<font color=gray><i> --separate-tilesets objectclass \ </i></font>
<font color=gray><i>tile \ </i></font>
<font color=gray><i>--style-mode property-based \ </i></font>
<font color=gray><i>--attributes all \ </i></font>
<font color=gray><i>--attribute-structure nested</i></font>
;
****: Separate Tilesets & Property-based Color Set & All Attributes in nested/json format
<font color=gray><i>--separate-tilesets objectclass tile \ </i></font>
<font color=gray><i>tile \ </i></font>
<font color=gray><i>--style-mode property-based \ </i></font>
<font color=gray><i>--attributes selected \ </i></font>
<font color=gray><i>--attribute-structure nested \ </i></font>
<font color=gray><i>--tiles-version 1.0 \ </i></font>
<font color=gray><i>--vertical-offset 3.5</i></font>
;



legend left
Recommended Datasets:
  Samplycity : https://muratkendir.github.io/samplycity/
  Hamburg LoD3 (CG2) : https://suche.transparenz.hamburg.de/dataset/3d-gebaeudemodell-lod3-0-hh-hamburg17
  Switzerland (CG2) : https://www.swisstopo.admin.ch/de/landschaftmodell-swissbuildings3d-3-0-beta#swissBUILDINGS3D-3.0-Beta---Download
endlegend

@endmindmap

```

## Former Tests

- Before release 0.9.3
    - [Tests done with Swisstopo dataset](https://www.3dcitydb.net/3dcitydb/fileadmin/public/kendir/#bern_full_procedure){:target="_blank"}
- Before release 0.9.2
    - [Tests done for SamplyCity Dataset](https://www.3dcitydb.net/3dcitydb/fileadmin/public/kendir/#test_campaign_03_samplycity){:target="_blank"}
- Test with Hamburg LoD3 dataset
    - [Hamburg Buildings LoD3](https://www.3dcitydb.net/3dcitydb/fileadmin/public/kendir/#test_campaign_02_hamburg){:target="_blank"}
- Test with Melbourne dataset
    - [Melbourne Buildings & Roads](https://www.3dcitydb.net/3dcitydb/fileadmin/public/kendir/#tests_for_3dtiler_melbourne){:target="_blank"}

