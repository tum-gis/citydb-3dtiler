# citydb-3dtiler

<blockquote>
Generates 3D Tiles by connecting to a 3DCityDB (v5) database instance with the provided custom arguments.
</blockquote>

<figure style="width:%100;text-align: center;">
  <img src="docs/images/cli_command_options_and_arguments_design_for_docs.drawio.png" alt="Usage" style="border:3px solid #005293">
  <figcaption>Using the Application (Semi-transparent sketched boxes indicate features that have not yet been implemented.)</figcaption>
</figure>

<hr>

<figure style="width:%100;text-align: center;">
  <img src="docs/images/app_mapp.svg" alt="Structure" style="border:3px solid #005293">
  <figcaption>Current Structure of Files & Folders</figcaption>
</figure>

<hr>

<figure style="width:%100;text-align: center;">
  <img src="docs/images/classes.svg" alt="UML Class Diagram" style="border:3px solid #005293">
  <figcaption>UML Class Diagram of the app</figcaption>
</figure>

<hr>

## Test Procedure

> Each command should be checked once when a milestone is achieved.

### 1. Check the **help** documentation

```bash
python3 citydb-3dtiler.py --help
```
<details>
<summary>1.1. Help doc for advise command</summary>

```bash
python3 citydb-3dtiler.py advise --help
```

</details>
<details>
<summary>1.2. Help doc for tile command</summary>

```bash
python3 citydb-3dtiler.py tile --help
```

</details>

### 2. Check the **advise** command

2.1. *advise for* **single tileset**

```bash
python3 citydb-3dtiler.py \
-H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 \
advise
```

2.2. *advise for* **separate tilesets**

2.2.1. *advise for separate tilesets* considering Object Classes

```bash
python3 citydb-3dtiler.py \
-H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 \
--separate-tilesets objectclass \
advise
```

### 3. Check the **tile** command

3.1. *tile as* **single tileset**

3.1.1. *tile as single tileset with* **Objectclass-based** *style-mode (default)*

```bash
python3 citydb-3dtiler.py \
-H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 \
--tilers-path tiler_app --tiler-app pg2b3dm \
tile \
--style-mode objectclass-based --style-absence-behavior fall-down
```

3.1.2. *tile as single tileset with* **property-based** *style-mode*

```bash
python3 citydb-3dtiler.py \
-H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 \
--tilers-path tiler_app --tiler-app pg2b3dm \
tile \
--style-mode property-based --style-absence-behavior fall-down
```

3.2. *tile as* **separate tilesets**

3.2.1. *tile as separate tilesets with* **objectclass-based** *style-mode (default)*

```bash
python3 citydb-3dtiler.py \
-H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 \
--tilers-path tiler_app --tiler-app pg2b3dm \
--separate-tilesets objectclass \
tile \
--style-mode objectclass-based --style-absence-behavior fall-down
```

3.2.2. *tile as separate tilesets with* **property-based** *style-mode*

```bash
python3 citydb-3dtiler.py \
-H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 \
--tilers-path tiler_app --tiler-app pg2b3dm \
--separate-tilesets objectclass \
tile \
--style-mode property-based --style-absence-behavior fall-down
```

<hr>
