import sqlite3

# Crear conexion con la base de datos
connection = sqlite3.connect('blog.db')
cur = connection.cursor()

# Realizar modificacion a la base de datos mediante SQL

# Modificacion realizada a la tabla posts
# cur.execute("""
#         CREATE TABLE posts (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#         title TEXT NOT NULL,
#         content TEXT NOT NULL,
#         author TEXT NOT NULL
#     )
# """)


# Modificacion realizada para eliminar los primeros post de prueba
# cur.execute("DELETE FROM posts WHERE id IN (1, 2, 3, 4)")

# Guardar los cambios y cerrar la conexión
connection.commit()
connection.close()