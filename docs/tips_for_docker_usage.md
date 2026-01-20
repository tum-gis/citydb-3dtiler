## Tips for Doker Usage

### Build


=== "Pattern"
    ```bash
    docker build --tag IMAGENAME:VERSIONorTAG .
    ```

=== "Sample"
    ```bash
    docker build -t citydb-3dtiler:0.9 .
    ```

### Run the Container

Pattern:

Sample:

```bash
docker run --rm --interactive \
--name citydb-3dtiler07 \
--volume ./:/home/citydb-3dtiler/shared:rw \
citydb-3dtiler:latest \
-H 10.162.246.195 -P 9876 -d citydb-visualizer \
-S citydb -u tester -p 123456 \
advise
```


### Check the Container itself (for development purposes)

Sample (Overwrite the Entrypoint):

```bash
docker run --rm --interactive --tty \
--volume ./:/home/citydb-3dtiler/shared:rw \
--name citydb-3dtiler09 \
--entrypoint /bin/bash \
citydb-3dtiler:latest
```

### Remove all the relevant containers, images etc.

All-in-One Command:

```bash
docker rm --force $(docker ps --all --quiet --filter label=composition=citydb-3dtiler) \
&& docker rmi --force $(docker image list --quiet --filter label=composition=citydb-3dtiler)
```
<details>
<summary>Remove Containers:</summary>

```bash
docker rm --force $(docker ps --all --quiet --filter label=composition=citydb-3dtiler)
```

</details>

<details>
<summary>Remove Images:</summary>

```bash
docker rmi --force $(docker image list --quiet --filter label=composition=citydb-visualizer)
```

</details>