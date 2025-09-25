#!/usr/bin/env python3
# incorporar_dados.py - Incorpora dados GeoJSON diretamente no HTML

import json
import os
from pathlib import Path

def incorporar_dados():
    """Incorpora dados do Ceará diretamente no HTML"""
    
    # Carrega dados do GeoJSON
    geojson_path = Path('data/ceara_municipios.geojson')
    if not geojson_path.exists():
        print("❌ Arquivo data/ceara_municipios.geojson não encontrado!")
        print("Execute primeiro: python abrir_mapa.py")
        return
    
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    print(f"✅ Carregados {len(geojson_data.get('features', []))} municípios")
    
    # Lê o HTML atual
    html_path = Path('index.html')
    if not html_path.exists():
        print("❌ Arquivo index.html não encontrado!")
        return
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Substitui a função loadMunicipalities para usar dados incorporados
    old_function = """async function loadMunicipalities() {
            try {
                const response = await fetch('data/ceara_municipios.geojson');
                const data = await response.json();
                
                data.features.forEach(feature => {
                    const name = feature.properties.name_muni || feature.properties.NM_MUN || feature.properties.NM_MUNICIP || feature.properties.municipio || feature.properties.name;
                    if (name) municipalities[name] = feature;
                });
                
                L.geoJSON(data, {
                    style: {fillColor: '#bbbbbb40', color: '#666666', weight: 0.6, fillOpacity: 0.2},
                    onEachFeature: function(feature, layer) {
                        const name = feature.properties.name_muni || feature.properties.NM_MUN || feature.properties.NM_MUNICIP || feature.properties.municipio || feature.properties.name;
                        if (name) {
                            layer.bindTooltip(name, {permanent: false, direction: 'center'});
                            layer.on('click', function(e) { handleMunicipalityClick(name, e.latlng); });
                        }
                    }
                }).addTo(map);
            } catch (error) {
                console.error('Erro ao carregar municípios:', error);
                showStatus('Erro ao carregar dados', 'error');
            }
        }"""
    
    # Cria a nova função com dados incorporados
    geojson_js = json.dumps(geojson_data, ensure_ascii=False)
    
    new_function = f"""function loadMunicipalities() {{
            try {{
                const data = {geojson_js};
                
                data.features.forEach(feature => {{
                    const name = feature.properties.name_muni || feature.properties.NM_MUN || feature.properties.NM_MUNICIP || feature.properties.municipio || feature.properties.name;
                    if (name) municipalities[name] = feature;
                }});
                
                L.geoJSON(data, {{
                    style: {{fillColor: '#bbbbbb40', color: '#666666', weight: 0.6, fillOpacity: 0.2}},
                    onEachFeature: function(feature, layer) {{
                        const name = feature.properties.name_muni || feature.properties.NM_MUN || feature.properties.NM_MUNICIP || feature.properties.municipio || feature.properties.name;
                        if (name) {{
                            layer.bindTooltip(name, {{permanent: false, direction: 'center'}});
                            layer.on('click', function(e) {{ handleMunicipalityClick(name, e.latlng); }});
                        }}
                    }}
                }}).addTo(map);
                
                console.log(`Carregados ${{Object.keys(municipalities).length}} municípios`);
            }} catch (error) {{
                console.error('Erro ao carregar municípios:', error);
                showStatus('Erro ao carregar dados', 'error');
            }}
        }}"""
    
    # Substitui no HTML
    new_html = html_content.replace(old_function, new_function)
    
    # Salva o novo HTML
    output_path = Path('mapa_ceara_completo.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ Mapa completo salvo em: {output_path}")
    print("🌐 Agora você pode abrir diretamente no navegador sem servidor!")
    
    return output_path

if __name__ == "__main__":
    incorporar_dados()
