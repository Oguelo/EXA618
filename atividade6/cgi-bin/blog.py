#!/usr/bin/env python3
import cgi
import cgitb
import datetime
import os

cgitb.enable()

ARQUIVO_DADOS = "mensagens.txt"

if not os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "w") as f:
        pass

form = cgi.FieldStorage()
autor = form.getvalue("autor")
mensagem = form.getvalue("mensagem")

if autor and mensagem:
    data_envio = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(ARQUIVO_DADOS, "a") as f:
        f.write(f"{autor}|{mensagem}|{data_envio}\n")

print("Content-Type: text/html; charset=utf-8\n")

print(f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Blog CGI</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        .post {{ border-bottom: 1px solid #ccc; padding: 10px 0; }}
        .meta {{ font-size: 0.8em; color: #666; }}
        form {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        input, textarea {{ width: 100%; margin-bottom: 10px; }}
        button {{ background: #28a745; color: white; border: none; padding: 10px; cursor: pointer; }}
    </style>
</head>
<body>
    <h1> Blog Teste 6</h1>
    
    <form method="GET" action="blog.py">
        <input type="text" name="autor" placeholder="Seu nome" required>
        <textarea name="mensagem" placeholder="Sua mensagem..." required></textarea>
        <button type="submit">Publicar Mensagem</button>
    </form>

    <hr>
    <h2>Mensagens Recentes</h2>
""")

if os.path.exists(ARQUIVO_DADOS):
    with open(ARQUIVO_DADOS, "r") as f:
        posts = f.readlines()
        for post in reversed(posts):
            parts = post.strip().split("|")
            if len(parts) == 3:
                autor, msg, data_msg = parts
                print(f"""
                <div class="post">
                    <strong>{autor}</strong> disse:
                    <p>{msg}</p>
                    <div class="meta">Postado em: {data_msg}</div>
                </div>
                """)

print("""
</body>
</html>
""")