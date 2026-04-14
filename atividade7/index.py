from flask import Flask, request, jsonify, render_template_string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os
import json

app = Flask(__name__)

def conectar_e_preparar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    
    creds_json = os.environ.get('GOOGLE_CREDS')
    if creds_json:
        info_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info_dict, scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    
    client = gspread.authorize(creds)
    sheet = client.open("Banco de dados - atividade7").sheet1

    
    if not sheet.cell(1, 1).value:
        cabecalhos = ["author", "message", "date"]
        sheet.insert_row(cabecalhos, 1)
    
    return sheet

@app.route('/api/put', methods=['POST'])
def api_put():
    dados = request.get_json()
    
    if not dados or dados.get("action") != "put":
        return jsonify({"status": "error", "message": "Ação inválida"}), 400
    
    autor = dados.get("author")
    mensagem = dados.get("message")
    
    if autor and mensagem:
        data_envio = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            sheet = conectar_e_preparar_planilha()
          
            sheet.append_row([autor, mensagem, data_envio])
            return jsonify({"status": "success"}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"status": "error", "message": "Campos faltando"}), 400

@app.route('/listagem')
@app.route('/')
def listar():
    try:
        sheet = conectar_e_preparar_planilha()
        
        registros = sheet.get_all_records() 
    except Exception as e:
        return f"Erro ao acessar a planilha: {e}"
 
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Blog API</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 40px auto; background: #fdfdfd; padding: 20px; }
            .post { border: 1px solid #4285f4; padding: 15px; margin-bottom: 10px; border-radius: 5px; background: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
            .header { color: #0f9d58; font-weight: bold; font-size: 1.1em; }
            .date { color: #888; font-size: 0.8em; margin-top: 10px; }
            p { margin: 10px 0; color: #333; }
        </style>
    </head>
    <body>
        <h1> Mensagens Enviadas</h1>
        <hr>
        {% if not posts %}
            <p>Nenhuma mensagem encontrada.</p>
        {% endif %}
        {% for r in posts %}
        <div class="post">
            <span class="header">{{ r.author }}</span> disse:
            <p>{{ r.message }}</p>
            <div class="date">Enviado em: {{ r.date }}</div>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, posts=reversed(registros))

if __name__ == '__main__':
    app.run(debug=True)