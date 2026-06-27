from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# CLAVE SECRETA
app.secret_key = '2o)XIwg}I$x]'

# CONFIGURACION MYSQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_gestion_vulnerabilidades'

mysql = MySQL(app)

# PAGINA PRINCIPAL

@app.route('/')
def inicio():
    return render_template('index.html')

# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT * FROM usuarios
            WHERE usuario = %s AND password = %s
        """, (usuario, password))

        usuario_encontrado = cursor.fetchone()

        if usuario_encontrado:

            session['usuario'] = usuario

            return redirect('/vulnerabilidades')

    return render_template('login.html')

# MOSTRAR VULNERABILIDADES

@app.route('/vulnerabilidades')
def vulnerabilidades():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM vulnerabilidades")

    datos = cursor.fetchall()

    return render_template(
        'vulnerabilidades.html',
        vulnerabilidades=datos
    )

# AGREGAR VULNERABILIDAD

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():

    if request.method == 'POST':

        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        severidad = request.form['severidad']

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO vulnerabilidades
            (nombre, descripcion, severidad, estado)
            VALUES (%s, %s, %s, %s)
        """, (nombre, descripcion, severidad, 'Pendiente'))

        mysql.connection.commit()

        return redirect('/vulnerabilidades')

    return render_template('agregar.html')

# MITIGAR VULNERABILIDAD

@app.route('/mitigar/<int:id>')
def mitigar(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE vulnerabilidades
        SET estado = 'Mitigada'
        WHERE id = %s
    """, (id,))

    mysql.connection.commit()

    return redirect('/vulnerabilidades')

# EJECUTAR

if __name__ == '__main__':
    app.run(debug=True)