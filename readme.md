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

Each command should be checked once when a milestone is achieved.

1. [ ] Check the help documentation

```bash
python3 citydb-3dtiler.py -H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 --tilers-path tiler_app --tiler-app pg2b3dm --help
```
<details>
<summary>Help doc for advise command</summary>

```bash
python3 citydb-3dtiler.py -H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 --tilers-path tiler_app --tiler-app pg2b3dm advise --help
```

</details>
<details>
<summary>Help doc for tile command</summary>

```bash
python3 citydb-3dtiler.py -H localhost -P 9876 -d citydb-visualizer -S citydb -u tester -p 123456 --tilers-path tiler_app --tiler-app pg2b3dm tile --help
```

</details>

<hr>

## Abbreviations used as Alias in SQL Blocks

- ftr : FeaTuRe
- oc : Object Class
- prp : PRoPerty
- mtr_ftr : MaTeRials for FeaTuRes
- mtr_prp : MaTeRials by PRoPerties