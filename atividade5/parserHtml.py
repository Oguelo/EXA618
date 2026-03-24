import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def gerar_agregador():
   
    with open('./atividade5/seeds.txt', 'r') as f:

        urls = [linha.strip() for linha in f if linha.strip() and not linha.startswith('[')]

    html_final = """
    <html>
    <head>
        <title>Imagens da Turma - EXA618</title>
        <style>
            .aluno { border: 1px solid #ccc; margin: 10px; padding: 10px; display: inline-block; width: 200px; vertical-align: top; }
            img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>Estudantes de Engenharia de Computação</h1>
    """

    for url in urls:
        try:
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as page:
                html_content = page.read().decode('utf-8')
            
    
            soup = BeautifulSoup(html_content, 'lxml')
            
            titulo = soup.title.string 
            
         
            primeira_img = soup.find('img')
            src_img = ""
            src_img = primeira_img.attrs.get("src")
               
            src_img = urljoin(url, src_img)
            
    
            html_final += f"""
            <div class="aluno">
                <img src="{src_img}">
                <p><strong>{titulo}</strong></p>
            </div>
            """
           

        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

    html_final += "</body></html>"

    with open('agregador.html', 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print("\nArquivo 'agregador.html' criado com sucesso!")

if __name__ == "__main__":
    gerar_agregador()