# Território Cearense – Mapa Interativo

Aplicação Streamlit para explorar o estado do Ceará com camadas de Municípios, Distritos e Bairros, além de registrar contagens (viaturas e motos) por município.

## Requisitos

- Python 3.10+
- Dependências do `requirements.txt`
- Dados GeoJSON já presentes em `data/`

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # no macOS/Linux
# no Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se usar Apple Silicon e tiver problemas com `geopandas/fiona`, considere instalar via conda/miniforge:

```bash
conda create -n territorio python=3.10 -y
conda activate territorio
conda install -c conda-forge geopandas osmnx -y
pip install streamlit folium pandas
```

## Executando

```bash
streamlit run app.py
```

A aplicação abre no navegador. Use a barra lateral para:
- Ativar/desativar camadas (Bairros, Distritos, Municípios)
- Selecionar um município e registrar contagens
- Baixar o CSV de contagens e o HTML do mapa

## Dados

- `data/ceara_municipios.geojson`
- `data/distritos_ceara_osm.geojson`
- `data/IBGE/bairros_ibge_ceara.geojson`

Scripts auxiliares:
- `download_bairros.py`: baixa distritos e bairros do OSM
- `aggregate_bairros.py`: agrega setores do IBGE em bairros oficiais
- `inspect_setores.py`: inspeção de colunas dos setores

## Observações

- O cache dos GeoJSON acelera a abertura. Limpe com “Rerun”/“Clear cache” se trocar os arquivos.
- Os nomes de município são obtidos a partir de múltiplas chaves comuns no GeoJSON.
# raio_territorio
