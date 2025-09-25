#!/usr/bin/env python3
# servidor.py - Servidor simples para o mapa interativo

import http.server
import socketserver
import os
import json
import requests
from urllib.parse import urlparse

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adiciona CORS headers para permitir requisições
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Se a requisição for para ceara_municipios.geojson e o arquivo não existir, baixa do GitHub
        if self.path == '/data/ceara_municipios.geojson':
            local_path = 'data/ceara_municipios.geojson'
            if not os.path.exists(local_path):
                try:
                    os.makedirs('data', exist_ok=True)
                    print("Baixando dados do Ceará...")
                    response = requests.get(
                        'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json',
                        timeout=30
                    )
                    response.raise_for_status()
                    
                    # Normaliza os nomes dos municípios
                    data = response.json()
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
                    
                    with open(local_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False)
                    print(f"Dados salvos em {local_path}")
                except Exception as e:
                    print(f"Erro ao baixar dados: {e}")
                    self.send_error(500, "Erro ao carregar dados")
                    return
        
        super().do_GET()

def main():
    PORT = 8000
    
    # Verifica se o arquivo HTML existe
    if not os.path.exists('index.html'):
        print("Erro: arquivo index.html não encontrado!")
        return
    
    # Cria o diretório data se não existir
    os.makedirs('data', exist_ok=True)
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Servidor rodando em http://localhost:{PORT}")
        print(f"Acesse: http://localhost:{PORT}/index.html")
        print("Pressione Ctrl+C para parar")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor parado.")

if __name__ == "__main__":
    main()
