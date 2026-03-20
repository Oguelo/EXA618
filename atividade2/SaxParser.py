import xml.sax
from time import perf_counter
import csv

class Listener(xml.sax.ContentHandler):
    def __init__(self):
    
        self.dados_extraidos = []
        self.lat = ""
        self.lon = ""
        self.nome = None
        self.tipo = None

    def startElement(self, tag, attributes):    
        if tag == "node":  
            self.lat = attributes.get("lat", "")
            self.lon = attributes.get("lon", "")
         
            self.tipo = None
            self.nome = None
            
        elif tag == "tag":
            k = attributes.get("k", "")
            v = attributes.get("v", "")
            if k == "amenity":
                self.tipo = v
            elif k == "name":
                self.nome = v

    def endElement(self, tag):    
        if tag == "node":  
            
            if self.tipo and self.nome:
                self.dados_extraidos.append([self.lat, self.lon, self.tipo, self.nome])


print("Starting SAX Parser...")
inicio = perf_counter()
estabelecimentosEncontrados = "EstabelecimentoEncontradosSax.csv"
parser = xml.sax.make_parser()
Handler = Listener()
parser.setContentHandler(Handler)


parser.parse("./atividade2/map.osm") 

tempo_total = perf_counter() - inicio


dados_finais = Handler.dados_extraidos

print(f"Foram encontrados {len(dados_finais)} estabelecimentos!")
print(f"Tempo SAX: {tempo_total:.4f} segundos\n")

with open(estabelecimentosEncontrados, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=',')
    escritor.writerow(['Latitude', 'Longitude', 'Tipo', 'Nome'])
    escritor.writerows(dados_finais)