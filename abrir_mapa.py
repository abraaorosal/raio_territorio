#!/usr/bin/env python3
# abrir_mapa.py - Abre o mapa diretamente no navegador

import webbrowser
import os
import json
import requests
from pathlib import Path

def download_geojson():
    """Baixa e normaliza o GeoJSON do Ceará"""
    local_path = Path('data/ceara_municipios.geojson')
    
    if local_path.exists():
        print("✅ Dados do Ceará já existem localmente")
        return
    
    try:
        print("📥 Baixando dados do Ceará...")
        response = requests.get(
            'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json',
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Normaliza nomes dos municípios
        for feat in data.get("features", []):
            props = feat.get("properties", {})
            name = (
                props.get("name_muni")
                or props.get("NM_MUN")
                or props.get("NM_MUNICIP")
                or props.get("municipio")
                or props.get("name")
            )
            if name:
                props["name_muni"] = name
                if not props.get("name"):
                    props["name"] = name
                feat["properties"] = props
        
        # Cria diretório e salva
        local_path.parent.mkdir(exist_ok=True)
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        print(f"✅ Dados salvos em {local_path}")
        
    except Exception as e:
        print(f"❌ Erro ao baixar dados: {e}")
        print("⚠️  O mapa funcionará, mas sem dados dos municípios")

def main():
    print("🗺️  CPRAIO - Distribuição Territorial")
    print("=" * 40)
    
    # Verifica se o arquivo HTML existe
    if not os.path.exists('index.html'):
        print("❌ Arquivo index.html não encontrado!")
        return

    # Baixa dados do Ceará
    download_geojson()

    # Abre no navegador
    html_path = os.path.abspath('index.html')
    file_url = f"file://{html_path}"
    
    print(f"🌐 Abrindo mapa em: {file_url}")
    print("📋 Funcionalidades disponíveis:")
    print("   • Pintar municípios com 5 cores diferentes")
    print("   • Marcar batalhões com ícones")
    print("   • Modo de edição para remover cores")
    print("   • Download do mapa em PDF")
    print("   • Estatísticas em tempo real")
    
    try:
        webbrowser.open(file_url)
        print("✅ Mapa aberto no navegador!")
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        print(f"💡 Abra manualmente: {file_url}")

if __name__ == "__main__":
    main()
