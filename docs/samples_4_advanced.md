# Example Commands for Advanced Users

This page lists sample commands used when testing the application with various datasets. Please note that some parameters, such as custom attribute names, may vary depending on the selected datasets.

## Difference between Docker Commands & Python Commands

This application has been published as Docker images in two different repositories and can also be run using only a Python virtual environment. Using the application is quite similar across all these platforms; however, only the first part of the commands will vary depending on the platform you choose. Therefore, we will list only the application arguments as example commands; however, keep in mind that you must combine these arguments with one of the platform-specific startup commands provided below:

### Start-Command(1) with the Docker Image Stored in Docker Hub

> If you'd like, you can replace the "latest" tag in the last row with any other fixed version number.

=== "Powershell"

    ```powershell
    docker run `
    --rm --interactive --tty `
    --name citydb-3dtiler `
    --volume ./:/home/tester/citydb-3dtiler/shared:rw `
    tumgis/citydb-3dtiler:latest `
    ```

=== "Linux Terminal"

    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    tumgis/citydb-3dtiler:latest \
    ```

=== "Command Prompt (CMD)"

    ```bash
    docker run ^
    --rm --interactive --tty ^
    --name citydb-3dtiler ^
    --volume ./:/home/tester/citydb-3dtiler/shared:rw ^
    tumgis/citydb-3dtiler:latest ^
    ```


### Start-Command(2) with the Docker Image Stored in GitHub Container Repo (GHCR)

> If you'd like, you can replace the "latest" tag in the last row with any other fixed version number.

=== "Powershell"

    ```powershell
    docker run `
    --rm --interactive --tty `
    --name citydb-3dtiler `
    --volume ./:/home/tester/citydb-3dtiler/shared:rw `
    ghcr.io/tum-gis/citydb-3dtiler:latest `
    ```

=== "Linux Terminal"

    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    ghcr.io/tum-gis/citydb-3dtiler:latest \
    ```

=== "Command Prompt (CMD)"

    ```bash
    docker run ^
    --rm --interactive --tty ^
    --name citydb-3dtiler ^
    --volume ./:/home/tester/citydb-3dtiler/shared:rw ^
    ghcr.io/tum-gis/citydb-3dtiler:latest ^
    ```


### Start-Command(3) with python virtual environment

> Do not forget to install python dependencies using ```pip install requirements.txt``` command.

=== "Powershell"

    ```powershell
    python citydb-3dtiler.py `
    ```

=== "Linux Terminal"

    ```bash
    python3 citydb-3dtiler.py \
    ```

=== "Command Prompt (CMD)"

    ```bash
    python citydb-3dtiler.py ^
    ```


## Samples

> You can change any of the parameters listed below as you see necessary. (For example: --db-host refers to the IP address or host name of the database server. Replace the IP address provided with the address of your own database.)

### Advise about Dataset - by <ins>separating</ins> the Tilesets - according to the <ins>ObjectClass</ins>'s

```bash
# Start-Command(1) or (2) or (3)
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--separate-tilesets objectclass \
advise
```


### Generate Tiles - by <ins>separating</ins> the Tilesets - according to the <ins>ObjectClass</ins>'s

```bash
# Start-Command(1) or (2) or (3)
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--separate-tilesets objectclass \
tile
```

### Generate Tiles - by *Filter*ing with - specific *ID*s ("objectid" in 3DCityDB)

```bash
# Start-Command(1) or (2) or (3)
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--id ID_B27AC6BF-787E-4AEC-A976-4B14660FEFC9,ID_A8A5F86D-B11C-4414-B671-19F7A8C854D9,ID_5973075F-DAF5-4979-BF91-B1CEE7AE1A6E \
tile
```