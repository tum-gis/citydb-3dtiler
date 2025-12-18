# citydb-3dtiler

<blockquote>
Generates 3D Tiles by connecting to a 3DCityDB (v5) database instance with the provided custom arguments.
</blockquote>

## How to use?

1. Download and (if it is a ZIP file) extract the repository

> If you don't want to customize the feature colors, skip to the Step 5. Otherwise follow the next instructions.

3. Check the file *materials_for_features/materials_for_features.ods* (with OpenOffice, LibreOffice or OnlyOffice) file and customize the colors just using the columns in the first sheet (Sheet Name: *materials*).

<details>
<summary>Alternatively ...</summary>

Open the document in LRZ Sync & Share:

https://syncandshare.lrz.de/getlink/fiWEn4L2VBQwFyVeqqFmRH/materials_for_features.ods

</details>

4. After making your customizations, export the spreadsheet as a CSV file and replace with the default file (*materails_for_features/materials_for_features.csv*).

<details>
<summary>Tips</summary>

- Field delimiter must be comma (,)
- Do not force to quote with apostrophe (").

</details>

5. Navigate into the same folder (citydb-3dtiler) with your favorite CLI tool (Terminal/Shell) using the ```cd FOLDERNAME``` command.

6. Pull the docker image with following command:

```bash
docker pull ghcr.io/muratkendir/citydb-3dtiler/citydb-3dtiler:0.9
```

7. Decide to which one of the following scenario best fits to your desire and replace the parameters given between the "<" and ">" characters.

You would like to ...

  7.1. create a **single** tileset by using **objectclass-based** materials

  <details>
  <summary>Commands for PowerShell</summary>
  Advise Command:
  
  ```bash
  docker run `
--rm --interactive `
--name citydb-3dtiler09 `
--volume ./materials_for_features:/home/tester/citydb-3dtiler/materials_for_features:rw `
--volume ./output:/home/tester/citydb-3dtiler/output `
ghcr.io/muratkendir/citydb-3dtiler/citydb-3dtiler:0.9 `
--db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> `
--db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> `
--db-username <USER-NAME> --db-password <DATABASE-PASSWORD> `
advise
  ```

  Tile Command:
  ```bash
  docker run `
  --rm --interactive `
  --name citydb-3dtiler09 `
  --volume ./materials_for_features:/home/tester/citydb-3dtiler/materials_for_features:rw `
  --volume ./output:/home/tester/citydb-3dtiler/output `
  ghcr.io/muratkendir/citydb-3dtiler/citydb-3dtiler:0.9 `
  --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> `
  --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> `
  --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> `
  tile
  ```
  </details>

  7.2. create a **single** tileset by using predefined (must be specified in CSV document) **property-based** materials

  7.3. create **separate** tilesets for every objectclasses using **objectclass-based** materials

  7.4. create **separate** tilesets for every objectclasses using predefined **property-based** materials

