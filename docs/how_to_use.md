# How to use?

## 1. Set the Feature Colors (Optional)

Download and customize the "materials_for_features" file with one of office software by changing the color values in the first sheet (sheet name : "materials").
    - [materials_for_features.ods](https://github.com/tum-gis/citydb-3dtiler/blob/main/materials_for_features/materials_for_features.ods)

> If you do not want to customize the feature colors (materials), proceed to Step 4. Otherwise, follow the next instructions.

??? info "Alternatively ..."
    Open the document in LRZ Sync & Share: <a href="https://syncandshare.lrz.de/getlink/fiWEn4L2VBQwFyVeqqFmRH/materials_for_features.ods" target="_blank">syncandshare.lrz.de/getlink/fiWEn4L2VBQwFyVeqqFmRH/materials_for_features.ods</a>


## 2. Save the ODS file as CSV

??? tip "Tips"
    - Field delimiters must be commas (,)
    - Do not force text to be quoted with apostrophes (")


## 3. Start the Terminal/Shell

Using your preferred CLI tool (Terminal/Shell), navigate to the same folder with the materials_for_features.csv. You can use the ```cd <FOLDERNAME>``` command to navigate to the folder.

## 4. Take an Advice for the Dataset (Optional)

(Optional) Create an advice file using the software. This advice file will summarize the existing object classes in your database and calculate the maximum features per tile.

=== "Powershell"

    ```powershell
    docker run `
    --rm --interactive --tty `
    --name citydb-3dtiler `
    --volume ./:/home/tester/citydb-3dtiler/shared:rw `
    ghcr.io/tum-gis/citydb-3dtiler:latest `
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> `
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> `
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> `
    advise
    ```

=== "Linux Terminal"

    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    ghcr.io/tum-gis/citydb-3dtiler:latest \
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> \
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> \
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> \
    advise
    ```

=== "Command Prompt (CMD)"

    ```bash
    docker run ^
    --rm --interactive --tty ^
    --name citydb-3dtiler ^
    --volume ./:/home/tester/citydb-3dtiler/shared:rw ^
    ghcr.io/tum-gis/citydb-3dtiler:latest ^
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> ^
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> ^
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> ^
    advise
    ```

=== "Sample Command"

    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    ghcr.io/tum-gis/citydb-3dtiler:latest \
    --db-host 10.162.246.888 --db-port 9876 \
    --db-name citydb-visualizer --db-schema citydb \
    --db-username tester2 --db-password louvre \
    advise
    ```


## 5. Generate the 3DTiles (using default configuration)

Generate 3DTiles using the default configuration by typing the following command: 

=== "Powershell"

    ```powershell
    docker run `
    --rm --interactive --tty `
    --name citydb-3dtiler `
    --volume ./:/home/tester/citydb-3dtiler/shared:rw `
    ghcr.io/tum-gis/citydb-3dtiler:latest `
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> `
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> `
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> `
    tile
    ```

=== "Linux Terminal"

    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    ghcr.io/tum-gis/citydb-3dtiler:latest \
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> \
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> \
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> \
    tile
    ```

=== "Command Prompt (CMD)"

    ```bash
    docker run ^
    --rm --interactive --tty ^
    --name citydb-3dtiler ^
    --volume ./:/home/tester/citydb-3dtiler/shared:rw ^
    ghcr.io/tum-gis/citydb-3dtiler:latest ^
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> ^
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> ^
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> ^
    tile
    ```

=== "Sample Command"

    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    ghcr.io/tum-gis/citydb-3dtiler:latest \
    --db-host 10.162.246.888 --db-port 9876 \
    --db-name citydb-visualizer --db-schema citydb \
    --db-username tester2 --db-password louvre \
    tile
    ```


If you need to use specify arguments see the page [Tiling Options](tiling_options.md)

## General Usage Options

??? example "citydb-3dtiler Usage"

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

## Remove the Docker Images

```bash
docker rmi --force $(docker image list --quiet --filter label=composition=citydb-3dtiler)
```