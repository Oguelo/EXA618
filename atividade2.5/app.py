from flask import Flask, request, make_response, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'EXA844' 

app.permanent_session_lifetime = timedelta(seconds=30)

config_acesso = {
    "usuario_permitido": "admin",
    "senha_permitida": "123"
}

@app.route('/')
def index():
    usuario_atual = session.get('user') or request.cookies.get('nome', 'visitante')
    
    chave_visitas = f'visitas_{usuario_atual}'
    contagem = int(request.cookies.get(chave_visitas, 0)) + 1
    
    html = f"""
        <h1>Olá, {usuario_atual}!</h1>
        <p>Visitas registradas para <strong>{usuario_atual}</strong>: {contagem}</p>
        <div id="status_sessao"></div>
        <hr>
        <p>Login configurado: <strong>{config_acesso['usuario_permitido']}</strong></p>
        <p><a href="/login">Ir para o Login</a></p>
        
        <script>
            if ("{session.get('user', '')}" !== "") {{
                let tempo = 30;
                document.getElementById('status_sessao').innerHTML = 
                    `<p style="color: red; font-weight: bold;">Sessão expira em: <span id="timer">30</span>s</p>`;
                
                const intervalo = setInterval(() => {{
                    tempo--;
                    document.getElementById('timer').innerText = tempo;
                    if (tempo <= 0) {{
                        clearInterval(intervalo);
                        window.location.href = '/logout';
                    }}
                }}, 1000);
            }}
        </script>
    """
    
    resp = make_response(html)
    resp.set_cookie(chave_visitas, str(contagem))
    resp.set_cookie('nome', usuario_atual)
    return resp

@app.route('/config_login/<novo_usuario>')
def mudar_credencial_login(novo_usuario):
    config_acesso["usuario_permitido"] = novo_usuario
    return redirect(url_for('index'))
   
@app.route('/nome/<novo_nome>')
def set_nome(novo_nome):
    if 'user' in session:
        session['user'] = novo_nome
    
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('nome', novo_nome)
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
      
        if usuario == config_acesso["usuario_permitido"] and senha == config_acesso["senha_permitida"]:
            session.permanent = True
            session['user'] = usuario
            
            resp = make_response(redirect(url_for('perfil')))
            resp.set_cookie('nome', usuario)
            return resp
        else:
            return f"<h3>Usuário inválido. Aceita-se apenas: {config_acesso['usuario_permitido']}</h3> <a href='/login'>Voltar</a>"

    return f'''
    <h2>Login (Usuário atual aceito: {config_acesso['usuario_permitido']})</h2>
    <form method="post">
        Usuário: <input type="text" name="usuario" required><br><br>
        Senha: <input type="password" name="senha" required><br><br>
        <input type="submit" value="Entrar">
    </form>
    '''

@app.route('/perfil')
def perfil():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return f"""
        <h1>Perfil</h1>
        <p>Logado como: <strong>{session['user']}</strong></p>
        <p><a href='/'>Início</a> | <a href='/logout'>Sair</a></p>
    """

@app.route('/logout')
def logout():
    session.pop('user', None)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('nome', 'visitante')
    return resp

if __name__ == '__main__':
    app.run(debug=True)