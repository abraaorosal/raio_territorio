# aggregate_bairros.py
import geopandas as gpd
import pandas as pd
from pathlib import Path

# 1) Carrega setores censitários do CE
shp_path = Path("data/IBGE/ce_setores_censitarios/23SEE250GC_SIR.shp")
gdf_set = gpd.read_file(shp_path)

# 2) Filtra apenas setores urbanos que possuem nome de bairro
gdf_set = gdf_set[
    (gdf_set["TIPO"] == "URBANO") & 
    (gdf_set["NM_BAIRRO"].notna())
]

# 3) Dissolve por nome de bairro (NM_BAIRRO)
gdf_bairros_ibge = (
    gdf_set
    .dissolve(by="NM_BAIRRO", as_index=False)
    [["geometry", "NM_BAIRRO"]]
    .rename(columns={"NM_BAIRRO": "bairro"})
)

# 4) Salva o GeoJSON resultante
out_path = Path("data/IBGE/bairros_ibge_ceara.geojson")
gdf_bairros_ibge.to_file(out_path, driver="GeoJSON")
print(f"Bairros oficiais salvos em {out_path} (total: {len(gdf_bairros_ibge)})")
