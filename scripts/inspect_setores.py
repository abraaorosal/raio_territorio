import geopandas as gpd

# 1. Carrega a malha de setores
gdf_set = gpd.read_file("data/IBGE/ce_setores_censitarios/23SEE250GC_SIR.shp")

# 2. Exibe colunas e primeiros registros
print("CRS:", gdf_set.crs)
print("Colunas disponíveis:", gdf_set.columns.tolist())
print("Amostra de 5 registros:\n", gdf_set.head()[["geometry"] + gdf_set.columns.tolist()[:5]])
