from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecreto'

# Usuarios ficticios con roles
USERS = {
    'profesor': {'password': 'profe123', 'role': 'profesor'},
    'estudiante': {'password': 'estu123', 'role': 'estudiante'}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        user_data = USERS.get(usuario)
        if user_data and user_data['password'] == contrasena:
            session['usuario'] = usuario
            session['rol'] = user_data['role']
            flash(f'Bienvenido, {usuario}', 'success')
            return redirect(url_for('dashboard'))

        flash('Credenciales incorrectas. Intenta nuevamente.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash('Primero debes iniciar sesión.', 'warning')
        return redirect(url_for('login'))

    usuario = session['usuario']
    rol = session['rol']
    return render_template('dashboard.html', usuario=usuario, rol=rol)

@app.route('/nueva-historia', methods=['GET', 'POST'])
def nueva_historia():
    if 'usuario' not in session:
        flash("Primero debes iniciar sesión.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Captura de datos omitida para este ejemplo
        flash("Historia clínica registrada correctamente.", "success")
        return redirect(url_for('dashboard'))

    return render_template('nueva_historia.html')

@app.route('/diagnostico_ia')
def diagnostico_ia():
    return render_template('diagnostico_ia.html')

@app.route('/reportes')
def reportes():
    if 'usuario' not in session:
        flash("Primero debes iniciar sesión.", "warning")
        return redirect(url_for('login'))
    return render_template('reportes.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
