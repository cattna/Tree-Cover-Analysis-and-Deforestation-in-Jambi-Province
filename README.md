# Tree-Cover-Analysis-and-Deforestation-in-Jambi-Province
This project aims to analyze tree cover change and deforestation in Jambi Province, Indonesia. By leveraging geospatial data and data analysis techniques, the project identifies areas experiencing significant tree cover loss, visualizes deforestation trends, and provides data to support mitigation efforts.

Certainly, based on your project context, here's a draft README description suitable for GitHub:

Tree Cover Analysis and Deforestation in Jambi Province
Project Description
This project aims to analyze tree cover change and deforestation in Jambi Province, Indonesia. By leveraging geospatial data and data analysis techniques, the project identifies areas experiencing significant tree cover loss, visualizes deforestation trends, and provides data to support mitigation efforts.

Key Features
Geospatial Analysis: Utilizes shapefile data to map administrative boundaries and tree cover areas.

Data Visualization: Generates interactive graphs and maps to visualize deforestation data.

Database Integration: Employs PostgreSQL with the PostGIS extension for efficient geospatial data storage and management.

Priority Area Identification: Highlights regions with the highest tree cover loss to focus mitigation efforts.

Project Structure
tree-cover-jambi/
├── batas_administrasi_jambi/
│   ├── batas_administasi_jambi.cpg
│   ├── batas_administasi_jambi.dbf
│   ├── batas_administasi_jambi.prj
│   ├── batas_administasi_jambi.qmd
│   ├── batas_administasi_jambi.shp
│   └── batas_administasi_jambi.shx
├── grafik_total.ipynb
└── output/
    ├── grafik_deforestasi_total.png
    └── peta_deforestasi_total.html
batas_administrasi_jambi/: Contains shapefile for Jambi Province's administrative boundaries.

grafik_total.ipynb: Jupyter Notebook containing code for data analysis and generating total tree cover loss graphs per regency/city.

output/: Directory for storing project outputs, such as graphs and HTML maps.

System Requirements
Python 3.x

Python libraries: rasterio, geopandas, pandas, matplotlib, rasterstats, folium,
