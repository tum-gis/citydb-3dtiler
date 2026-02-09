# citydb-3dtiler

This application can create 3DTiles (v 1.0 and 1.1) by reading features (aka. city objects) from 3DCityDB (v5.x), a database application that can import CityGML 2.0 or 3.0-based datasets. The application's key features are as follows:
- It can generate summary reports by reading the database or calculate the most efficient configuration parameters for creating 3D Tiles.
- It can assign colors or (PBR) materials based on object classes or the current property values of features.
- It can create separate 3DTiles based on object classes.
- Tilesets can be customized with a simple CSV file listing materials.

<figure style="width:%100;text-align: center;">
  <img src="docs/images/sample_3dtiles_leipzig.jpg" alt="Sample 3DTiles from Leipzig" style="border:3px solid #4CAE4F">
  <figcaption>A set of tilesets represents the city objects of Leipzig city</figcaption>
</figure>

<blockquote>
Links for relevant libraries :
<ul>
	<li>3DCityDB: <a href="https://docs.3dcitydb.org/edge/" target="_blank">docs.3dcitydb.org/edge</a> </li>
	<li>pg2b3dm: <a href="https://github.com/Geodan/pg2b3dm" target="_blank">github.com/Geodan/pg2b3dm</a> </li>
</ul>
</blockquote>

## Documentation

Please check the documentation page available here:
[citydb-3dtiler Docs](https://tum-gis.github.io/citydb-3dtiler/)

Docker image of the application is available. Check the following pages for more information:
- [How to use the application within Docker](https://tum-gis.github.io/citydb-3dtiler/how_to_use_w_docker/)
- [Tips for Docker Usage](https://tum-gis.github.io/citydb-3dtiler/tips_for_docker_usage/)

## Special Thanks:

This application is based on two important concepts and aims to bridge the gap between the concepts 3DTiles and CityGML.
To bridge this gap, two main elements have been used in this software:

1. 3DCityDB v5
2. pg2b3dm

***We would like to take this opportunity to thank Bert Temme, the developer of the pg2b3dm library, and all 3DCityDB developers.***
