# citydb-3dtiler

!!! warning "This application is in the testing phase"

    This application is still in the testing phase. Please exercise caution when using it in production. Therefore, feedback is always welcome. Please feel free to create an issue on the GitHub page or contact me: murat.kendir(At)tum.de

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
  <img src="./images/cli_command_options_and_arguments_design_for_docs.drawio.svg" alt="Usage" style="border:3px solid #005293">
  <figcaption>Using the Application (Semi-transparent sketched boxes indicate features that have not yet been implemented.)</figcaption>
</figure>
 
## Documentation

- [How to use with Docker?](how_to_use_w_docker.md)
- [How to use with VENV?](how_to_use_w_venv.md)
- [All Commands & Samples](all_commands_samples.md)
- [Tips for Docker Usage](tips_for_docker_usage.md)
- [Test Procedures & Sample Tilesets](test_procedures.md)
- [Documentation for the Developers](developer_docs.md)

## Special Thanks

This application is based on two important concepts and aims to bridge the gap between the concepts 3DTiles and CityGML.
To bridge this gap, two main elements have been used in this software:

1. 3DCityDB v5
2. pg2b3dm

***We would like to take this opportunity to thank Bert Temme, the developer of the pg2b3dm library, and all 3DCityDB developers.***