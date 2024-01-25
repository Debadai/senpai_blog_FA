from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {"autor": "Joaquin", "texto": "sjidbcsbdc"},
    {"autor": "Ines", "texto": "jshdcbsd"},
    {"autor": "Nico", "texto": "sdncisdhic"},
    {"autor": "Andres", "texto": "jidnvidjnfv"},
    {"autor": "Maria", "texto": "jisdnvjfn"},
    {"autor": "Juan", "texto": "djhvnhfvd"},
]

@app.route('/')
def home():
    return render_template('home.html', nombre="Joaquin", posts=posts)

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

app.run()