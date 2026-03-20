import json
import csv 
geojson = {
    "type": "FeatureCollection",
    "features": []
}


with open('EstabelecimentoEncontradosSax.csv', mode='r', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.DictReader(arquivo_csv)
    id = 0
    for linhas in leitor_csv:

        geometry = dict()
        geometry["type"] = "Point"
        geometry["coordinates"] = [
            float(linhas["Longitude"]), 
            float(linhas["Latitude"])]

        propriedades =dict()
        propriedades["nome"] = linhas["Nome"]
        propriedades["tipo" ]= linhas["Tipo"]

        feature = dict()
        feature["type"] = "Feature"
        feature["geometry"] = geometry
        feature["properties"] = propriedades
        feature["id"] = id
        geojson["features"].append(feature)
        id += 1


jsonStr = json.dumps(geojson, indent=4, ensure_ascii=False)

# 1) Salvar o arquivo GeoJSON (para você anexar na atividade)
with open('atividade4_geo.json', 'w', encoding='utf-8') as f:
    f.write(jsonStr)