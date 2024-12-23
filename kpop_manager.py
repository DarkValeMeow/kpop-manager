import sqlite3
import os
import random

# Colores ANSI para la terminal
RESET = "\033[0m"
BOLD = "\033[1m"
PINK = "\033[95m"
CYAN = "\033[96m"
PURPLE = "\033[94m"

# Verificar si la base de datos existe sin eliminarla
db_path = "kpop.db"

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Creación de tablas (solo si no existen)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Artista (
    id_artista INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    debut DATE NOT NULL,
    pais TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Cancion (
    id_cancion INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    duracion REAL NOT NULL CHECK (duracion > 0),
    genero TEXT NOT NULL,
    fecha_lanzamiento DATE NOT NULL,
    rating_fans REAL NOT NULL CHECK (rating_fans BETWEEN 0 AND 10),
    rating_profesional REAL NOT NULL CHECK (rating_profesional BETWEEN 0 AND 10)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Album (
    id_album INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    cantidad_canciones INTEGER NOT NULL,
    id_artista INTEGER NOT NULL,
    fecha_lanzamiento DATE NOT NULL,
    rating REAL NOT NULL CHECK (rating BETWEEN 0 AND 10),
    FOREIGN KEY (id_artista) REFERENCES Artista (id_artista)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Artista_Cancion (
    id_artista INTEGER,
    id_cancion INTEGER,
    PRIMARY KEY (id_artista, id_cancion),
    FOREIGN KEY (id_artista) REFERENCES Artista (id_artista),
    FOREIGN KEY (id_cancion) REFERENCES Cancion (id_cancion)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Cancion_Album (
    id_cancion INTEGER,
    id_album INTEGER,
    PRIMARY KEY (id_cancion, id_album),
    FOREIGN KEY (id_cancion) REFERENCES Cancion (id_cancion),
    FOREIGN KEY (id_album) REFERENCES Album (id_album)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Fan (
    id_fan INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Fan_Artista (
    id_fan INTEGER,
    id_artista INTEGER,
    PRIMARY KEY (id_fan, id_artista),
    FOREIGN KEY (id_fan) REFERENCES Fan (id_fan),
    FOREIGN KEY (id_artista) REFERENCES Artista (id_artista)
);
''')

# Inserción de datos ficticios solo si están vacíos
cursor.execute("SELECT COUNT(*) FROM Artista")
if cursor.fetchone()[0] == 0:
    cursor.executemany('''
    INSERT INTO Artista (id_artista, nombre, debut, pais) VALUES (?, ?, ?, ?)
    ''', [
        (1, "Twice", "2015-10-20", "Corea del Sur"),
        (2, "Red Velvet", "2014-08-01", "Corea del Sur"),
        (3, "Ateez", "2018-10-24", "Corea del Sur")
    ])

cursor.execute("SELECT COUNT(*) FROM Cancion")
if cursor.fetchone()[0] == 0:
    cursor.executemany('''
    INSERT INTO Cancion (id_cancion, nombre, duracion, genero, fecha_lanzamiento, rating_fans, rating_profesional) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1, "Keeper", 3.7, "Pop", "2024-12-06", 8.7, 8.6),
        (2, "Cosmic", 4.1, "Pop", "2024-08-01", 9.5, 9.2),
        (3, "Pirate King", 3.9, "K-Pop", "2018-10-24", 8.5, 8.4)
    ])

cursor.execute("SELECT COUNT(*) FROM Fan")
if cursor.fetchone()[0] == 0:
    nombres_fans = ["Jiwoo", "Sangmin", "Hyerin", "Minji", "Jisoo", "Seonghwa", "Yunho", "Wooyoung", "San"]
    edades_fans = [random.randint(18, 30) for _ in range(len(nombres_fans))]
    artistas_fans = [1, 2, 3, 1, 2, 3, 1, 2, 3]

    fan_data = [(i + 1, nombres_fans[i], edades_fans[i]) for i in range(len(nombres_fans))]
    fans_artista = [(i + 1, artistas_fans[i]) for i in range(len(nombres_fans))]

    cursor.executemany('''
    INSERT INTO Fan (id_fan, nombre, edad) VALUES (?, ?, ?)
    ''', fan_data)

    cursor.executemany('''
    INSERT INTO Fan_Artista (id_fan, id_artista) VALUES (?, ?)
    ''', fans_artista)

conn.commit()

# Funciones para mostrar datos
def mostrar_informacion_grupo():
    cursor.execute("SELECT nombre, debut, pais FROM Artista")
    grupos = cursor.fetchall()
    print(f"\n{CYAN}Informacion de los Grupos:{RESET}")
    print("===========================")
    for grupo in grupos:
        print(f"{PURPLE}Nombre:{RESET} {grupo[0]}")
        print(f"{PURPLE}Debut:{RESET} {grupo[1]}")
        print(f"{PURPLE}Pais:{RESET} {grupo[2]}\n")

def mostrar_cancion_favorita():
    cursor.execute('''
    SELECT 
        Cancion.nombre AS cancion,
        Artista.nombre AS artista,
        Album.nombre AS album,
        Cancion.rating_fans AS rating
    FROM Cancion
    JOIN Artista_Cancion ON Cancion.id_cancion = Artista_Cancion.id_cancion
    JOIN Artista ON Artista_Cancion.id_artista = Artista.id_artista
    JOIN Cancion_Album ON Cancion.id_cancion = Cancion_Album.id_cancion
    JOIN Album ON Cancion_Album.id_album = Album.id_album
    ORDER BY rating DESC
    LIMIT 1;
    ''')
    favorita = cursor.fetchone()
    print(f"\n{CYAN}Cancion Favorita:{RESET}")
    print("=================")
    print(f"{PURPLE}Titulo:{RESET} {favorita[0]}")
    print(f"{PURPLE}Artista:{RESET} {favorita[1]}")
    print(f"{PURPLE}Album:{RESET} {favorita[2]}")
    print(f"{PURPLE}Rating Fans:{RESET} {favorita[3]}\n")

def mostrar_top_canciones():
    cursor.execute('''
    SELECT 
        Cancion.nombre AS cancion,
        Artista.nombre AS artista,
        Album.nombre AS album,
        Cancion.rating_fans AS rating
    FROM Cancion
    JOIN Artista_Cancion ON Cancion.id_cancion = Artista_Cancion.id_cancion
    JOIN Artista ON Artista_Cancion.id_artista = Artista.id_artista
    JOIN Cancion_Album ON Cancion.id_cancion = Cancion_Album.id_cancion
    JOIN Album ON Cancion_Album.id_album = Album.id_album
    ORDER BY rating DESC;
    ''')
    canciones = cursor.fetchall()
    print(f"\n{CYAN}Top Canciones Reproducidas:{RESET}")
    print("===========================")
    for i, cancion in enumerate(canciones, start=1):
        print(f"{PINK}{i}.{RESET} Cancion: {cancion[0]}")
        print(f"   {PINK}Artista:{RESET} {cancion[1]}")
        print(f"   {PINK}Album:{RESET} {cancion[2]}")
        print(f"   {PINK}Rating Fans:{RESET} {cancion[3]}\n")

def mostrar_todas_canciones_con_genero():
    cursor.execute('''
    SELECT 
        Cancion.nombre AS cancion,
        Cancion.genero AS genero,
        Artista.nombre AS artista
    FROM Cancion
    JOIN Artista_Cancion ON Cancion.id_cancion = Artista_Cancion.id_cancion
    JOIN Artista ON Artista_Cancion.id_artista = Artista.id_artista
    ORDER BY Cancion.genero;
    ''')
    canciones = cursor.fetchall()
    print(f"\n{CYAN}Canciones con Genero:{RESET}")
    print("======================")
    for cancion in canciones:
        print(f"{PURPLE}Cancion:{RESET} {cancion[0]}")
        print(f"{PURPLE}Genero:{RESET} {cancion[1]}")
        print(f"{PURPLE}Artista:{RESET} {cancion[2]}\n")

def mostrar_fans_por_grupo():
    cursor.execute('''
    SELECT Artista.nombre AS grupo, Fan.nombre AS fan, Fan.edad AS edad
    FROM Fan_Artista
    JOIN Fan ON Fan_Artista.id_fan = Fan.id_fan
    JOIN Artista ON Fan_Artista.id_artista = Artista.id_artista
    ORDER BY grupo, fan;
    ''')
    fans_por_grupo = cursor.fetchall()

    print(f"\n{CYAN}Fans organizados por grupo:{RESET}")
    print("==========================")

    grupo_actual = None
    for grupo, fan, edad in fans_por_grupo:
        if grupo != grupo_actual:
            grupo_actual = grupo
            print(f"\n{PURPLE}{grupo}:{RESET}")
        print(f"  - {PINK}{fan}{RESET}, {edad} años")

# Menú principal
def menu():
    while True:
        print(f"\n{CYAN}Favorite Songs Manager{RESET}")
        print(f"{CYAN}============================={RESET}")
        print(f"{PINK}1.{RESET} Ver informacion de los grupos")
        print(f"{PINK}2.{RESET} Ver cancion favorita")
        print(f"{PINK}3.{RESET} Ver top canciones")
        print(f"{PINK}4.{RESET} Ver canciones por gener")
        print(f"{PINK}5.{RESET} Ver fans de los grupos")
        print(f"{PINK}6.{RESET} Salir")
        opcion = input(f"{CYAN}Seleccione una opcion:{RESET} ")

        if opcion == "1":
            mostrar_informacion_grupo()
        elif opcion == "2":
            mostrar_cancion_favorita()
        elif opcion == "3":
            mostrar_top_canciones()
        elif opcion == "4":
            mostrar_todas_canciones_con_genero()
        elif opcion == "5":
            mostrar_fans_por_grupo()
        elif opcion == "6":
            print(f"{PURPLE}Saliendo del programa...{RESET}")
            break
        else:
            print(f"{PINK}Opcion invalida. Intente de nuevo.{RESET}")

if __name__ == "__main__":
    menu()

# Guardar cambios y cerrar conexión
conn.close()
