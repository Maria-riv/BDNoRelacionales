import vertica_python
import json

conn_info = {'host': 'localhost',
             'port': 5433,
             'user': 'dbadmin',
             'password': 'password',
             'database': 'dbName'}

# Establecer conexión
with vertica_python.connect(**conn_info) as connection:
    cur = connection.cursor()

    # Crear una tabla con una columna de tipo JSON
    cur.execute("""
        CREATE TABLE if not exists user_profiles (
            id INT,
            profile JSON
        )
    """)
    
    # Insertar datos JSON
    profile = json.dumps({'name': 'John Doe', 'age': 28, 'interests': ['cycling', 'hiking']})
    cur.execute("INSERT INTO user_profiles (id, profile) VALUES (1, %s)", (profile,))
    
    # Consultar y manipular datos JSON
    cur.execute("SELECT profile->>'name' as name FROM user_profiles WHERE id = 1")
    for row in cur.fetchall():
        print(row)
    
    # Actualizar datos JSON
    new_profile = json.dumps({'name': 'Jane Doe', 'age': 30, 'interests': ['reading', 'traveling']})
    cur.execute("UPDATE user_profiles SET profile = %s WHERE id = 1", (new_profile,))
    
    # Eliminar datos
    cur.execute("DELETE FROM user_profiles WHERE id = 1")
    
    # Cerrar la conexión
    cur.close()
