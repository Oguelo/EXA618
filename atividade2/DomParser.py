from time import perf_counter
import xml.sax
import csv
from xml.dom.minidom import parse

EstabelecimentosEncontradosDom = "estabelecimentosEncontradosDom.csv"

print("Starting DOM Parser...")


inicio = perf_counter()

MapaAnalisado = parse('./atividade2/map.osm')

dados_extraidos = []

for node in MapaAnalisado.getElementsByTagName("node"): 
    lat = node.getAttribute("lat")
    lgt = node.getAttribute("lon")
    tipo = None
    nome = None
    
    for tag in node.getElementsByTagName("tag"):
        k = tag.getAttribute("k")
        v = tag.getAttribute("v")
        
        if k == "amenity":
            tipo = v
        elif k == "name":
            nome = v
            
    if tipo and nome:
        dados_extraidos.append([lat, lgt, tipo, nome])

tempoFinal = perf_counter() - inicio
print(f"Foram encontrados {len(dados_extraidos)} estabelecimentos!")
print(f"Tempo total do DOM: {tempoFinal:.4f} segundos")



with open(EstabelecimentosEncontradosDom, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=',')
    escritor.writerow(['Latitude', 'Longitude', 'Tipo', 'Nome'])
    escritor.writerows(dados_extraidos)

