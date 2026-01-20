# Tiling Options

???+ example "citydb-3dtiler Usage"

    --help </br>
    --db-.. </br>
    ??? example "Database Connection Arguments"
        --db-host </br>
        --db-port (default: 5432) </br>
        --db-name </br>
        --db-schema (default: citydb) </br>
        --db-username </br>
        --db-password </br>
    --separate-tilesets
    ??? info "Separate Tilesets Options"
        None (Default) </br>
        objectclass
    --tiler-app (default: pg2b3dm) </br>
    --tilers-path (default: tiler_app) </br>
    advise </br>
    ??? example "Advise Arguments"
        --consider-thematic-features (default: False) </br>
        --output (default: advise.yml)
    tile
    ??? example "Tile Arguments"
        --style-mode
        ??? info "Style Mode Options"
            property-based </br>
            objectclass-based (default) </br>
            no-style
        --style-absence-behavior
        ??? info "Style Absence Behavior"
            falldown (default)
            riseup
        --transparency-mode
        ??? info "Transparency Options"
            Blend </br>
            Opaque (default)
        --output (default: shared/current folder)


Decide which of the following scenarios best suits your needs and modify the parameters in the tag style (<>).

<details>
<summary>Tips</summary>

If your 3DCityDB is running in another Docker container and has a port forwarded to your host machine (check this with the ```docker ps``` command), you can connect by entering the host machine's local IP address and the forwarded port number in the following instructions.

</details>

You would like ...

  6.1. to create a **single** tileset, taking into account all features available in 3DCityDB.

  <details>
  <summary>Advise command for PowerShell</summary>
  
  ```bash
  docker run `
  --rm --interactive `
  --name citydb-3dtiler09 `
  --volume ./:/home/tester/citydb-3dtiler/shared:rw `
  ghcr.io/tum-gis/citydb-3dtiler:0.9 `
  --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> `
  --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> `
  --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> `
  advise
  ```

  </details>

  6.2. to create **separate** tilesets for each object class available in 3DCityDB.

  <details>
  <summary>Advise command for PowerShell</summary>
  
  ```bash
  docker run `
  --rm --interactive `
  --name citydb-3dtiler09 `
  --volume ./:/home/tester/citydb-3dtiler/shared:rw `
  ghcr.io/tum-gis/citydb-3dtiler:0.9 `
  --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> `
  --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> `
  --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> `
  --separate-tilesets objectclass `
  advise
  ```

  </details>

7. Check the *output* folder and review the advice document. Then, decide which style mode best suits your needs.

You would like ...

  7.1. to create tilesets using **objectclass-based** materials.

  <details>
  <summary>Tile Command for PowerShell</summary>
  
  > Remove the last row the previous command ("advise") and add the followings:

  ```bash
  tile `
  --style-mode objectclass-based `
  --style-absence-behavior fall-down
  ```
  </details>

  7.2. to create tilesets using **property-based** materials. (Properties must be specified in the CSV file.)

  <details>
  <summary>Tile Command for PowerShell</summary>

  > Remove the last row the previous command ("advise") and add the followings:

  ```bash
  tile \
  --style-mode property-based --style-absence-behavior fall-down
  ```

  </details>