## Tips for Docker Usage

### Build


=== "Pattern"
    ```bash
    docker build --tag IMAGENAME:VERSIONorTAG .
    ```

=== "Sample"
    ```bash
    docker build -t citydb-3dtiler:custom-build .
    ```

### Run the Container (once)

=== "Powershell"
    ```powershell
    docker run `
    --rm --interactive --tty `
    --name citydb-3dtiler `
    --volume ./:/home/tester/citydb-3dtiler/shared:rw `
    citydb-3dtiler:latest `
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
    citydb-3dtiler:latest \
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
    citydb-3dtiler:latest ^
    --db-host <IP-or-COMP-NAME> --db-port <PORT-NUMBER> ^
    --db-name <DATABASE-NAME> --db-schema <SCHEMA-NAME> ^
    --db-username <USER-NAME> --db-password <DATABASE-PASSWORD> ^
    advise
    ```

=== "Sample Command"
    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler07 \
    --volume ./:/home/citydb-3dtiler/shared:rw \
    citydb-3dtiler:latest \
    -H 10.162.246.888 -P 9876 -d citydb-visualizer \
    -S citydb -u tester -p 123456 \
    advise
    ```


### Check the container contents (for development purposes)

Following commands will execute the container with bash, so you can investigate the contents of the container:

=== "Powershell"
    ```powershell
    docker run `
    --rm --interactive --tty `
    --name citydb-3dtiler `
    --volume ./:/home/tester/citydb-3dtiler/shared:rw `
    --entrypoint /bin/bash `
    citydb-3dtiler:latest `
    ```

=== "Linux Terminal"
    ```bash
    docker run \
    --rm --interactive --tty \
    --name citydb-3dtiler \
    --volume ./:/home/tester/citydb-3dtiler/shared:rw \
    --entrypoint /bin/bash \
    citydb-3dtiler:latest
    ```

=== "Command Prompt (CMD)"
    ```bash
    docker run ^
    --rm --interactive --tty ^
    --name citydb-3dtiler ^
    --volume ./:/home/tester/citydb-3dtiler/shared:rw ^
    --entrypoint /bin/bash ^
    citydb-3dtiler:latest
    ```

=== "Sample Command"
    ```bash
    docker run --rm --interactive --tty \
    --volume ./:/home/citydb-3dtiler/shared:rw \
    --name citydb-3dtiler:latest \
    --entrypoint /bin/bash \
    citydb-3dtiler:latest
    ```

### Remove all the relevant containers, images etc.

Remove all at once:

```bash
docker rm --force $(docker ps --all --quiet --filter label=composition=citydb-3dtiler) \
&& docker rmi --force $(docker image list --quiet --filter label=composition=citydb-3dtiler)
```
<details>
<summary>Remove only containers:</summary>

```bash
docker rm --force $(docker ps --all --quiet --filter label=composition=citydb-3dtiler)
```

</details>

<details>
<summary>Remove only images:</summary>

```bash
docker rmi --force $(docker image list --quiet --filter label=composition=citydb-3dtiler)
```

</details>
