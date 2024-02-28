import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Funciones para la base de datos

def get_db_connection():
    """
    Crea la conexion con la base de datos, se utiliza dentro de las otras funciones.
    """
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_all(query, params=None):
    """
    Solicita dos argumentos, query y params. Se conecta a la base de datos y ejecuta la query (esta ya esta escrita con un str) con los params (parametros) ingresados.
    Si no hay params (parametros) ejecuta un SELECT * (todos).
    """
    conn = get_db_connection()
    cursor = conn.execute(query, params) if params else conn.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def insert(query, params):
    """
    Solicita dos argumentos, query y params. Se conecta a la base de datos y ejecuta la query (esta ya esta escrita con un str) con los params (parametros) ingresados.
    Cuando se ejecuta dentro de la tabla de registro, solicita los parametros usuario y contrasena.
    Cuando se ejecuta dentro de la tabla de post, solicita los parametros autor, titulo y contenido.
    """
    conn = get_db_connection()
    conn.execute(query, params)
    conn.commit()
    conn.close()

# Rutas a los templates

@app.route('/')
def home():
    """
    Renderiza la home. Si hay posteos en la tabla posts, los muestra ordenados segun la fecha de creacion.
    """
    titulo_busqueda = request.args.get('search')
    if titulo_busqueda:
        query = "SELECT * FROM posts WHERE posts.title LIKE ? ORDER BY created DESC"
        params = (f"%{titulo_busqueda}%",)
        posts = query_all(query, params)
    else:
        posts = query_all("SELECT * FROM posts ORDER BY created DESC")
    return render_template("home.html", posts=posts)

@app.route('/contact')
def contact():
    """
    Renderiza la pagina de contacto.
    """
    return render_template("contact.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Renderiza la pagina de login. Los metodos pueden ser GET o POST. En caso de GET renderiza al usuario el panel para ingresar sus credenciales,
    en caso de POST valida las credenciales y redirige a la pagina del perfil. En caso de no validar las credenciales muestra un mensaje de error.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_query = "SELECT * FROM users WHERE username = ?"
        user = query_all(user_query, (username,))
        if user and user[0]['password'] == password:
            session['username'] = username # En esta linea almaceno al usuario en la sesion
            return redirect('/profile')
        else:
            # Solo pasa el mensaje de error si las credenciales son incorrectas.
            return render_template("login.html", error="Usuario o contraseña incorrecta")

    # En este caso estamos en GET. No pasa la variable error si es la primera vez que se carga la página.
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Renderiza la pagina de register. Los metodos pueden ser GET o POST. En caso de GET renderiza al usuario el panel para registrarse.
    En caso de POST realiza las validaciones de usuario y contraseña cumplan con los requisitos. En caso de exito agrega el usuario a la base de datos,
    le muestra un mensaje y renderiza la pagina de inicio de sesion. En caso de error muestra un mensaje para que el usuario pueda intentar nuevamente.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if not username or not password:
            return render_template("register.html", error="El username y el password son obligatorios")
        
        if len(password) < 5:
            return render_template("register.html", error="La password debe contener más de 5 caracteres")
        
        if " " in username:
            return render_template("register.html", error="El nombre de usuario no puede contener espacios")
        
        if not any(c.isalpha() for c in password):
            return render_template("register.html", error="La password debe contener al menos una letra")
        
        if not any(c.isdigit() for c in password):
            return render_template("register.html", error="La password debe contener al menos un numero")
        
        user_query = "SELECT * FROM users WHERE users.username == ?"
        existing_user = query_all(user_query, (username,))
        if not existing_user:
            insert("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return render_template("register.html", exito="Usuario creado con éxito!")
        return render_template("register.html", error="El username ya existe")

    return render_template("register.html")

@app.route('/profile')
def profile():
    """
    Renderiza la pagina de profile. El usuario tiene que estar logueado, en caso contrario redirige al login.
    """
    if 'username' in session:
        return render_template("profile.html", username=session['username'])
    return redirect('/login')

@app.route('/logout', methods=["POST"])
def logout():
    """
    Esta funcion elimina elimina al usuario de la sesion.
    """
    session.pop('username', None)
    return redirect('/')

@app.route('/post', methods=["GET", "POST"])
def create_post():
    """
    Permite al usuario crear un nuevo post, admite los metodos GET y POST. Primero verifica que el usuario este logueado en la sesion, en caso contrario renderiza la pagina de login con un mensaje
    solicitando al usuario que se loguee. Si el metodo es POST, toma los datos del titulo y el contenido ingresados por el usuario, a la vez que toma el dato del autor como el username de la sesion.
    Luego inserta el registro en la tabla posts de la base de datos.
    """
    if 'username' not in session:
        return render_template("login.html", error="Por favor, inicie sesion para publicar un post.")

    if request.method == "POST":
        title = request.form["titulo"]
        content = request.form["contenido"]
        author = session['username']

        if title and content:
            insert("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))
            return redirect('/')
        else:
            return render_template("post.html", error="Todos los campos son obligatorios")

    # Si el método es GET, renderiza la página para crear un nuevo post.
    return render_template("post.html")


@app.route('/post/<id>')
def post_id(id):
    """
    Renderiza el post seleccionado por id, haciendo la consulta a la base de datos.
    """
    post_query = "SELECT * FROM posts WHERE posts.id == ?"
    post = query_all(post_query, (id,))
    if post:
        return render_template("post.html", post=post[0])
    return redirect('/')

app.run(debug=True)