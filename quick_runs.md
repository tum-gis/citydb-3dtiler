# All Commands that has been used during tests

## citydb-visualizer commands

### Ordinary Docker Start Command for citydb-visualizer

```bash
docker run --name citydb-visualizer \
--detach \
--shm-size=16g \
--publish 8080:80 \
--publish 9876:5432 \
-e POSTGRES_HOST=localhost -e POSTGRES_PORT=5432 \
-e POSTGRES_DB=citydb-visualizer \
-e POSTGRES_USER=tester -e POSTGRES_PASSWORD=123456 \
-e SRID=25832 -e GMLSRSNAME="urn:ogc:def:crs:EPSG::25832" \
--volume "./citygml_data/:/home/tester/citygml_data" \
--volume "./sql_queries:/home/tester/sql_queries" \
--volume "./tiling_commands:/home/tester/tiling_commands" \
--volume "./terrain_tileset/:/var/www/html/3dcitydb-web-map-2.0.0/examples/terrain_tileset" \
--volume "./tilesets/:/var/www/html/3dcitydb-web-map-2.0.0/examples/tilesets" \
citydb-visualizer:0070
```

### Fine-Tuned Docker Container :
```bash
docker run --name citydb-visualizer \
--shm-size=16g \
--detach \
--publish 8080:80 \
--publish 9876:5432 \
-e POSTGRES_HOST=localhost -e POSTGRES_PORT=5432 \
-e POSTGRES_DB=citydb-visualizer \
-e POSTGRES_USER=tester -e POSTGRES_PASSWORD=123456 \
-e SRID=25832 -e GMLSRSNAME="urn:ogc:def:crs:EPSG::25832" \
--volume "./citygml_data/:/home/tester/citygml_data" \
--volume "./sql_queries:/home/tester/sql_queries" \
--volume "./tiling_commands:/home/tester/tiling_commands" \
--volume "./terrain_tileset/:/var/www/html/3dcitydb-web-map-2.0.0/examples/terrain_tileset" \
--volume "./tilesets/:/var/www/html/3dcitydb-web-map-2.0.0/examples/tilesets" \
citydb-visualizer:0070 \
-c work_mem=43690kB \
-c shared_buffers=4GB \
-c max_parallel_workers=8 \
-c effective_cache_size=12GB \
-c wal_buffers=16MB
```

```bash
docker exec --interactive --tty citydb-visualizer /home/tester/scripts/12_import_all.sh
```

## citydb-3dtiler commands

### for single tileset
```bash
docker run \
--rm --interactive --tty \
--name citydb-3dtiler09 \
--volume ./:/home/tester/citydb-3dtiler/shared:rw \
ghcr.io/tum-gis/citydb-3dtiler:latest \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer --db-schema citydb \
--db-username tester --db-password 123456 \
tile
```

### for separate tilesets
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--separate-tilesets objectclass \
tile
```

### filter by id(s)
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--id _20210907161723_295,_20210907161723_1,_20210907161723_220 \
tile
```

### filter by TypeName (ObjectClass)
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name WallSurface,OuterFloorSurface,OuterCeilingSurface \
tile \
--tiles-version 1.0
```

### limit the total feature number
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--limit 1000 \
tile \
--tiles-version 1.0
```

### use start-index
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--start-index 200000 \
tile \
--tiles-version 1.0
```

### use limit and start-index together
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--limit 100000 --start-index 200000 \
tile \
--tiles-version 1.0
```

### use type-name, limit and start-index together
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name WallSurface,OuterFloorSurface,OuterCeilingSurface,RoofSurface \
--limit 100000 --start-index 200000 \
tile \
--tiles-version 1.0
```

### use bbox filtering with CRS code
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 564822,5932935,566924,5934737,25832 \
tile \
--tiles-version 1.0
```

### use bbox filtering without CRS code
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 564822,5932935,566924,5934737 \
tile
```

### use bbox filtering in intersects-precise mode
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 564822,5932935,566924,5934737,25832 \
--bbox-mode intersects-precise \
tile
```

### use bbox filtering with contains mode
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 564822,5932935,566924,5934737,25832 \
--bbox-mode contains \
tile
```

### use bbox filtering with contains-precise mode
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 564822,5932935,566924,5934737,25832 \
--bbox-mode contains-precise \
tile
```

### use filter argument to use CQL2 Expressions
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name Building \
--filter "gen_grundhoehenn > '20' AND gen_grundflaeche2d > '30'" \
tile \
--tiles-version 1.0 \
--attributes selected \
--selected-attributes gen_grundhoehenn,gen_grundflaeche2d
```

### use filter argument to use CQL2 Expressions 2
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name Building \
--filter "s_within(st_envelope(~geom),BBOX(564573, 5933311, 565095, 5933739,25832))" \
tile \
--tiles-version 1.0 \
--attributes selected \
--selected-attributes gen_grundhoehenn,gen_grundflaeche2d
```

### use filter argument to use CQL2 Expressions 3
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name Building \
--filter "s_crosses(st_envelope(~geom),LINESTRING(564919 5933223, 565387 5934847))" \
tile \
--tiles-version 1.0 \
--attributes selected \
--selected-attributes gen_grundhoehenn,gen_grundflaeche2d
```

### use sql-filter
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name Building \
--sql-filter "gen_citygrid_unitid.pro_value like '2021%' AND st_dwithin(st_geomfromtext('POINT(566924 5934737)',25832), ~geom, 2000)" \
tile \
--tiles-version 1.0 \
--attributes selected \
--selected-attributes gen_citygrid_unitid
```

### use sql-filter 2
```bash
python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name Building \
--sql-filter "st_dwithin(st_geomfromtext('POINT(566924 5934737)',25832), ~geom, 2000)" \
tile \
--tiles-version 1.0 
```

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--type-name GroundSurface,WallSurface,RoofSurface \
tile

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 2593748,1196992,2595958,1198506,2056 \
tile

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 2593748,1196992,2598168,1200021,2056 \
--bbox-mode contains-precise \
tile

BBOX (Swiss) Part A: 2593748,1196992,2595958,1200021,2056
BBOX (Swiss) Part B: 2595958,1196992,2598168,1200021,2056
BBOX (Swiss) Part A+B: 2593748,1196992,2598168,1200021,2056

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--filter "gen_revision_jahr >= 2021" \
tile \
--attributes selected \
--selected-attributes gen_dach_min

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
--bbox 2593748,1196992,2595958,1198506,2056 \
tile

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
tile

python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
advise


python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
tile \
--attributes all

--separate-tilesets objectclass \

time python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
advise

time python3 citydb-3dtiler.py \
--db-host 10.162.246.195 --db-port 9876 \
--db-name citydb-visualizer \
--db-schema citydb \
--db-username tester --db-password 123456 \
tile \
--vertical-offset 1.0