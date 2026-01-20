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


