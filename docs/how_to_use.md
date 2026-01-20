# citydb-3dtiler

<blockquote>
Generates 3D Tiles by connecting to a 3DCityDB (v5) database instance by considering the provided arguments (separation, material colors etc.).

Links for relevant libraries :
<ul>
<li>3DCityDB: <a href="https://docs.3dcitydb.org/edge/" target="_blank">docs.3dcitydb.org/edge</a> </li>
<li>pg2b3dm: <a href="https://github.com/Geodan/pg2b3dm" target="_blank">github.com/Geodan/pg2b3dm</a> </li>
</ul>
</blockquote>

## Development Progress

The following diagram shows the application's currently available and unavailable but planned features.

<figure style="width:%100;text-align: center;">
  <img src="../images/cli_command_options_and_arguments_design_for_docs.drawio.svg" alt="Usage" style="border:3px solid #005293">
  <figcaption>Using the Application (Semi-transparent sketched boxes indicate features that have not yet been implemented.)</figcaption>
</figure>

## How to use?

1. (Optional) Download and customize the "materials_for_features" file with one of office software by changing the color values in the first sheet (sheet name : "materials").
  - [materials_for_features.ods](https://github.com/tum-gis/citydb-3dtiler/blob/main/materials_for_features/materials_for_features.ods)

> If you do not want to customize the feature colors (materials), proceed to Step 4. Otherwise, follow the next instructions.

<details>
<summary>Alternatively ...</summary>

Open the document in LRZ Sync & Share:
<a href="https://syncandshare.lrz.de/getlink/fiWEn4L2VBQwFyVeqqFmRH/materials_for_features.ods" target="_blank">syncandshare.lrz.de/getlink/fiWEn4L2VBQwFyVeqqFmRH/materials_for_features.ods</a>
</details>


2. Save as the ODS file as CSV.

<details>
<summary>Tips</summary>
<ul>
<li>Field delimiters must be commas (,)</li>
<li>Do not force text to be quoted with apostrophes (")</li>
</ul>
</details>


4. Using your preferred CLI tool (Terminal/Shell), navigate to the same folder (citydb-3dtiler) using the ```cd <FOLDERNAME>``` command.

5. Pull the docker image with following command:

```bash
docker pull ghcr.io/tum-gis/citydb-3dtiler:0.9
```

6. Decide which of the following scenarios best suits your needs and modify the parameters in the tag style (<>).

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
  --volume ./materials_for_features:/home/tester/citydb-3dtiler/materials_for_features:rw `
  --volume ./output:/home/tester/citydb-3dtiler/output `
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
  --volume ./materials_for_features:/home/tester/citydb-3dtiler/materials_for_features:rw `
  --volume ./output:/home/tester/citydb-3dtiler/output `
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


## Special Thanks:

This application is based on two important concepts and aims to bridge the gap between the concepts 3DTiles and CityGML.
To bridge this gap, two main elements have been used in this software:

1. 3DCityDB v5
2. pg2b3dm

***We would like to take this opportunity to thank Bert Temme, the developer of the pg2b3dm library, and all 3DCityDB developers.***