import os
from pathlib import Path
import geopandas as gpd
import osmnx as ox

# Cria pasta de saída
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

# 1) Geocode da área do Ceará
area = ox.geocode_to_gdf("Ceará, Brazil")

# 2) Tags para limites administrativos de nível 8 (distritos) e 9 (bairros)
tags = {
    "boundary": "administrative",
    "admin_level": ["8", "9"]
}

# 3) Baixar feições do OSM dentro do polígono do Ceará
gdf_osm = ox.features_from_polygon(area.geometry.iloc[0], tags)

# 4) Filtrar polígonos
gdf_osm = gdf_osm[gdf_osm.geom_type.isin(["Polygon", "MultiPolygon"])]

# 5) Separar distritos e bairros
gdf_distritos = gdf_osm[gdf_osm["admin_level"] == "8"].copy()
gdf_bairros   = gdf_osm[gdf_osm["admin_level"] == "9"].copy()

# 6) Salvar arquivos GeoJSON
distritos_path = output_dir / "distritos_ceara_osm.geojson"
bairros_path   = output_dir / "bairros_ceara_osm.geojson"
gdf_distritos.to_file(distritos_path, driver="GeoJSON")
gdf_bairros.to_file(bairros_path, driver="GeoJSON")

print(f"Distritos salvos em {distritos_path}")
print(f"Bairros   salvos em {bairros_path}")
