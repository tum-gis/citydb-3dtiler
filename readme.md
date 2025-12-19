# citydb-3dtiler

<blockquote>
Generates 3D Tiles by connecting to a 3DCityDB (v5) database instance by considering the provided arguments (separation, material colors etc.).
</blockquote>

## How to use?

1. Download and extract the repository (if it is a ZIP file).

> If you don't want to customize the feature colors, skip to the Step 4. Otherwise follow the next instructions.

2. Check the file *materials_for_features/materials_for_features.ods* (with OpenOffice, LibreOffice or OnlyOffice) file and customize the colors just using the columns in the first sheet (Sheet Name: *materials*).

<details>
<summary>Alternatively ...</summary>

Open the document in LRZ Sync & Share:

https://syncandshare.lrz.de/getlink/fiWEn4L2VBQwFyVeqqFmRH/materials_for_features.ods

</details>

3. After making your customizations, export the spreadsheet as a CSV file and replace with the default file (*materails_for_features/materials_for_features.csv*).

<details>
<summary>Tips</summary>

- Field delimiter must be comma (,)
- Do not force to quote with apostrophe (").

</details>

4. Navigate into the same folder (citydb-3dtiler) with your favorite CLI tool (Terminal/Shell) using the ```cd <FOLDERNAME>``` command.

5. Pull the docker image with following command:

```bash
docker pull ghcr.io/tum-gis/citydb-3dtiler:0.9
```

6. Decide to which one of the following scenario best fits to your desire and replace the parameters given between the "<" and ">" characters.

You would like to ...

  6.1. (Sin) create a **single** tilesets by considering every available object in 3DCityDB.

  <details>
  <summary>Advise command for PowerShell</summary>
  
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

  </details>

  6.2. (Sep) create **separate** tilesets for every objectclasses in 3DCityDB

  <details>
  <summary>Advise command for PowerShell</summary>
  
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
  --separate-tilesets objectclass `
  advise
  ```

  </details>

7. Check the *output* folder to see the advise document. After that, decide to which one of the following scenario best fits to your desire.

  7.1. (Obj) create tilesets considering **objectclass-based** materials

  <details>
  <summary>Tile Command for PowerShell</summary>
  
  > Remove the last row the previous command ("advise") and add the followings:

  ```bash
  tile `
  --style-mode objectclass-based `
  --style-absence-behavior fall-down
  ```
  </details>

  7.2. (Pro) create tilesets considering predefined **property-based** materials

  <details>
  <summary>Tile Command for PowerShell</summary>

  > Remove the last row the previous command ("advise") and add the followings:

  ```bash
  tile \
  --style-mode property-based --style-absence-behavior fall-down
  ```

  </details>

