from flask import Flask, flash, render_template, redirect, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app = Flask(__name__, template_folder='templates')
app.secret_key = 'makolindoMonstro' #Senha para os cookies de sessão

#Configuração do servidor de e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nathancielusinski@gmail.com'
app.config['MAIL_PASSWORD'] = 'odrj jtum ytbc zaii'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

#Serializador para gerar os tokens seguros
serial = URLSafeTimedSerializer(app.secret_key)

#Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

#Rota para solicitar a redefinição de senha
@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']

        #Preparação e envio do e-mail
        token = serial.dumps(email, salt='password_recovery')
        msg = Message('Recuperação de senha', sender='nathancielusinski@gmail.com', recipients=[email])
        link = url_for('reset_password', token=token, _external=True)
        msg.body = f'Clique no link a seguir para redefinir sua senha: {link}'
        mail.send(msg)

        flash('Um link de recuperação de senha foi enviado para o seu e-mail.', category='success')

        return redirect(url_for('index'))
    
    return render_template('reset_password.html')

#Rota para redefinir a senha
@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password_token(token):
    try:
        email = serial.loads(token, salt='password_recovery', max_age=3600)
    except SignatureExpired:
        flash('O link de recuperação de senha expirou.', category='error')
        return redirect(url_for('reset_password'))
    except BadSignature:
        flash('Link inválido.', category='error')
        return redirect(url_for('reset_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        flash('Senha alterada com sucesso.', category='success')
        return redirect(url_for('index'))
    return render_template('reset.html')

if __name__ == '__main__':
    app.run(debug=True)