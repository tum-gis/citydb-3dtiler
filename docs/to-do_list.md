# Notes for myself

> Done : ✔  |  Cancelled : ✗  |  Postponed : 😴 | Milestone ✌️


- 30.10.2025
  - [✔] move the database connection checks into another file or into citydb-3dtiler
  - [✔] change the single quotation marks with double quotation marks
  - [✔] document the other files
  - [✔] move the generic writer and reader functions to another file such as helper_io or something else.
  - [✔] Prepare the class diagram for the SQL encapsulations.
  - [✔] Change the "ignore" arguments in the usage diagram to reflect the changes in args.

- 31.10.2025
  - [✔] try to project simpliest SQL query on the classes.

- 03.11.2025
  - [✔] check the diagrams.
  - [✔] implement the "separate-tilesets" argument.
  - [✔] query the available objectclasses.
  - [😴] query the available namespaces.

- 05.11.2025
  - [✔] implement run_query func in the advise_main.py
    - run_sql and run_query stored as separate functions. (returns nothing and returns results)
- 10.11.2025
  - [✔] implement filter for the set_kernel()
- 18.11.2025
  - [✔] Refresh the visuals regarding the new classes.
- 24.11.2025
  - [✔] Change the name of "run_query" in pg_connection as "get_query_results"
  - [✔] Implement the normal advise mechanism
  - [✔] Repeat the objectclass based separation in tiling
- 25.11.2025
  - [✔] Implement the new advisement classes (ABC classes) into the separate-tilesets option in advisement.
  - [✔] Reactivate the YAML rewriting.
- 26.11.2025
  - [✌️] Take a beer, first tileset has been created.
- 27.11.2025
  - [✔] Time to start implement styling-options...
- 11.12.2025
  - [✔] Change the name of "advise_sql" as "standalone_queries"
  - [✔] Add query names to the info "SQL Query executed."
  - [✔] Remove the (i)--> Connection Status messages.
  - [😴] Think about adding a "controller" package...
  - [ ] Complete the existing-appearances scenario.
- 12.12.2025
  - [✔] Check that terms are used consistently
- 14.12.2025
  - [✔] Refactor tile_main.py>51 (property based materials)
- 16.12.2025
- [✔] No need for the CompositeQueryBlock (QueryBlock supports nested queries by self)
- [✔] Create a docker image !
- [✔] Fix the advise command to calculate a "max feature per tile" value, even if it is executed for separated tilesets.
- [😴] Fix the typo : Advise --> Advice
- 20.01.2026
- [✔] Activate the custom-style argument
- [✔] Add a controller for the absence of advise document
- 21.01.2026
- [✔] Check the documentation pages and test the commands
- [✔] Add the Test Procedure to Docs
- [✔] Update the graphics regarding to the new argument names
- [✔] Publish the repo as public
- 27.01.2026
- [ ] When an overlayed object is opaque while other is transparent, transparent mode is not working. Ask it to Bert Temme.
- [ ] Implement the Web Map Client to the docker image as an instant viewer
- [✔] Check the emissive color option. (not urgent, Thomas said the object are a bit dark.)
- [ ] Test with FZKHaus LOD3 building model.
- [ ] Filter out the linestring objects.
- [ ] Vertical polygon-parts of the multipolygons are causing an issue. Check if you can tesselate them as TIN.