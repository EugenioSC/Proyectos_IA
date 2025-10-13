import sqlite3

# --- CONEXIÓN A LA BASE DE DATOS ---
conn = sqlite3.connect('restaurante.db')
cursor = conn.cursor()

# --- CREACIÓN DE TODAS LAS TABLAS ---

cursor.execute("""
CREATE TABLE IF NOT EXISTS tipos_preparacion (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS platos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    tipo_id INTEGER,
    FOREIGN KEY(tipo_id) REFERENCES tipos_preparacion(id)
)
""")

cursor.execute("CREATE TABLE IF NOT EXISTS origenes (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE)")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    cantidad INTEGER DEFAULT 0,
    origen_id INTEGER,
    disponible INTEGER DEFAULT 1,
    FOREIGN KEY(origen_id) REFERENCES origenes(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS plato_ingredientes (
    plato_id INTEGER,
    ingrediente_id INTEGER,
    FOREIGN KEY(plato_id) REFERENCES platos(id),
    FOREIGN KEY(ingrediente_id) REFERENCES ingredientes(id),
    PRIMARY KEY (plato_id, ingrediente_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre_usuario TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS preferencias_ingredientes (
    usuario_id INTEGER,
    ingrediente_id INTEGER,
    puntuacion INTEGER CHECK(puntuacion >= 1 AND puntuacion <= 5),
    PRIMARY KEY (usuario_id, ingrediente_id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(ingrediente_id) REFERENCES ingredientes(id)
)
""")

print("Todas las tablas han sido creadas y/o verificadas correctamente.")

try:
    # Categorías y orígenes
    cursor.execute("INSERT OR IGNORE INTO tipos_preparacion (nombre) VALUES ('Natural'), ('Horneado'), ('Freído'), ('Vapor')")
    cursor.execute("INSERT OR IGNORE INTO origenes (nombre) VALUES ('Vegetal'), ('Animal'), ('Marino')")

  
    cursor.execute("""
    INSERT OR IGNORE INTO ingredientes (nombre, cantidad, origen_id) VALUES
    ('Arroz de sushi', 1000, 1), ('Alga nori', 100, 1), ('Aguacate', 50, 1),
    ('Cangrejo', 50, 3), ('Anguila', 30, 3), ('Camarón', 60, 3),
    ('Queso Crema', 40, 2), ('Res', 50, 2), ('Philadelphia', 50, 2),
    ('Tocino', 50, 2), ('California', 50, 1), ('Chile Caribe', 10, 1),
    ('Topping de queso gratinado', 20, 2), ('Aderezo Miso', 10, 1),
    ('Ajonjolí negro', 5, 1), ('Pulpo', 20, 3), ('Surimi empanizado', 20, 3),
    ('Cebollín', 5, 1), ('Arare', 5, 1), ('Tampico topping', 5, 1),
    ('Salsa roja', 10, 1), ('Green sauce', 10, 1), ('Salsa balsámica', 5, 1),
    ('Cebolla caramelizada', 5, 1), ('Atún', 30, 3), ('Salmón', 30, 3),
    ('Chiles', 10, 1),

    -- Ingredientes nuevos añadidos
    ('Queso Americano', 20, 2), ('Queso Chihuahua', 20, 2), ('Queso Gouda', 20, 2),
    ('Camarón Empanizado', 20, 3), ('Camarones Empanizados', 20, 3), ('Camarones Fritos', 20, 3),
    ('Camarones Rellenos Philadelphia', 20, 3), ('Kanikama Osaki', 20, 3), ('Kanikama', 20, 3),
    ('Masago', 10, 3), ('Dedos de Queso Empanizados', 20, 2), ('Res Frita', 20, 2),
    ('Aderezo Volcánico', 10, 1), ('Aderezo Especial', 10, 1), ('Aderezo Cilantro', 10, 1),
    ('Aderezo Spicy', 10, 1), ('Salsa Sriracha', 10, 1), ('Spicy Calamar Capeado', 10, 3),
    ('Callo Spicy', 10, 3), ('Rajitas', 10, 1), ('Limón', 10, 1),
    ('Tampico', 10, 1), ('Tampico Spicy', 10, 1), ('Camarón Spicy', 10, 3),
    ('Plátano Macho', 10, 1), ('Pasta de Camarón', 10, 3), ('Ajonjolí blanco', 10, 1),
    ('Salsa Caramelo', 10, 1), ('Chile Serrano', 10, 1)
    """)

    # Platos 
    cursor.execute("""
    INSERT OR IGNORE INTO platos (nombre, descripcion, tipo_id) VALUES
    ('Rollo California', 'El clásico rollo con pepino, aguacate y cangrejo.', 1),
    ('Dragon Roll', 'Rollo de anguila horneada sobre un rollo de tempura.', 2),
    ('Rollo Tempura', 'Rollo de camarón y queso crema, completamente freído.', 3),
    ('Mar y tierra', 'Camarón, res, philadelphia y aguacate por dentro.', 3),
    ('Chon', 'Aguacate, camarón y res por dentro; philadelphia, cangrejo y queso gratinado por fuera; con aderezo miso y ajonjolí.', 3),
    ('Cordon blue', 'Pollo, tocino, aguacate y philadelphia por dentro; philadelphia y queso gratinado por fuera.', 3),
    ('Camarón blue', 'Camarón, tocino y aguacate por dentro; philadelphia, tocino y queso gratinado por fuera.', 3),
    ('Monster Roll', 'California, camarón en tempura, aguacate y chile caribe por dentro; cangrejo y philadelphia por fuera; topping de queso gratinado spicy, salsa de anguila y aderezo miso.', 3),
    ('Avocado Tuna Roll', 'Aguacate por fuera; california y aguacate por dentro; topping de atún spicy, camarón jumbo capeado en ajonjolí; aderezo green, salsa de anguila y balsámico.', 1),
    ('Bonito Roll', 'Aguacate, pepino, aguacate, philadelphia, camarón, surimi empanizado, california, puntos de salsa roja, salsa de anguila, ajonjolí negro y aderezo spicy.', 1),
    ('Guamuchilito', 'Pulpo, camarón y philadelphia por fuera; camarón, cangrejo, aguacate y pepino por dentro; guamuchilito topping y ajonjolí; con un rayado de salsa de anguila y puntos de aderezo spicy.', 1),
    ('Señorita Roll', 'Atún y aguacate por fuera; camarón jumbo en tempura, aguacate y california por dentro; topping de cebollín, arare, salsa de anguila y aderezo spicy.', 1),
    ('Guerra', 'Camarón, philadelphia, aguacate por fuera; camarón empanizado, aguacate y pepino por dentro; tampico topping y ajonjolí.', 1),
    ('Caramelo Hot', 'Envuelto en surimi y philadelphia; camarón empanizado, pepino y aguacate por dentro; bañado en salsa caramelo, ajonjolí, aderezo de cilantro y salsa roja.', 2),
    ('Green Hot', 'Envuelto en aguacate; philadelphia, aguacate y pepino por dentro; topping de pasta de camarón, tocino con aderezo green, salsa de anguila y ajonjolí negro.', 2),
    ('Avocado Hot', 'Aguacate por fuera; philadelphia, aguacate y pepino por dentro; topping de camarón spicy, ajonjolí blanco y salsa de anguila.', 2),
    ('Salmoncito Hot', 'Salmón horneado por fuera; pepino, philadelphia y aguacate por dentro; topping spicy de camarón, ajonjolí blanco y salsa de anguila.', 2),
    ('Banano Hot', 'Envuelto en plátano macho; aguacate, pepino, philadelphia y cebolla caramelizada por dentro; topping de camarón, ajonjolí, aderezo spicy y salsa de anguila.', 2),
    ('Tres quesos', 'Pepino, aguacate, res, camarón, philadelphia, queso americano, queso gratinado', 3),
    ('Norteño', 'Philadelphia, pepino, aguacate, camarón empanizado, queso gratinado, res, tocino y chile serrano', 3),
    ('Avocado eby', 'Philadelphia, Pepino, Aguacate, tampico spisy y camarones rellenos con Philadelphia', 1),
    ('Oranger taiguer', 'Philadelphia, aguacate, Chile caribe, tampico, camarón, spicy de calamar capeado, ajonjolí y salsa de anguila', 1),
    ('Chica light', 'pepino, aguacate, tampico, camarones empanizados, Philadelphia, atún, salmón, kanikama osaki, masago y cebollín.', 1),
    ('El patrón', 'Pepino, camarón Empanizado, Philadelphia, rajitas, aguacate, camarón, Kanikama, callo spicy, limón, salsa sriracha y salsa de anguila.', 1),
    ('Lava hot', 'Philadelphia, pepino, aguacate, res, aderezo volcánico y camarones fritos.', 2),
    ('Carnívoro', 'Philadelphia, pepino, aguacate, pollo, tocino, queso gouda, queso chihuahua y res frita', 2),
    ('Salvaje hot', 'Philadelphia, pepino, aguacate, Res, pollo, camarón, Queso chihuahua, tampico, aderezo especial, salsa de anguila y chile serrano.', 2),
    ('Krack hot', 'Pepino, aguacate, dedos de queso empanizados, res, Philadelphia, aderezo especial, tocino y salsa de anguila', 2)
    """)

    # Plato-ingredientes
    plato_ingredientes = [
        (1,1),(1,2),(1,3),(1,4),
        (2,1),(2,2),(2,5),
        (3,1),(3,6),(3,7),
        (4,6),(4,8),(4,9),(4,3),
        (5,3),(5,6),(5,8),(5,9),(5,7),(5,15),
        (6,10),(6,11),(6,3),(6,9),(6,7),
        (7,6),(7,11),(7,3),(7,10),(7,7),
        (8,1),(8,6),(8,3),(8,12),(8,4),(8,9),(8,7),
        (9,3),(9,1),(9,4),(9,26),(9,6),(9,12),(9,23),
        (10,3),(10,2),(10,3),(10,7),(10,6),(10,16),(10,1),(10,20),(10,5),
        (11,17),(11,6),(11,7),(11,4),(11,3),(11,1),(11,18),(11,19),
        (12,26),(12,3),(12,6),(12,1),(12,17),(12,5),(12,7),
        (13,6),(13,7),(13,3),(13,6),(13,1),(13,3),(13,19),
        (14,16),(14,7),(14,6),(14,3),(14,19),(14,18),(14,20),
        (15,3),(15,7),(15,6),(15,11),(15,23),(15,5),(15,19),
        (16,3),(16,7),(16,6),(16,12),(16,5),(16,19),
        (17,25),(17,7),(17,3),(17,12),(17,5),(17,19),
        (18,3),(18,1),(18,7),(18,22),(18,6),(18,18),(18,20),

        # Nuevos platillos (IDs del 19 al 28)
        (19,3),(19,7),(19,6),(19,8),(19,27),(19,28),(19,13),
        (20,9),(20,3),(20,6),(20,31),(20,13),(20,8),(20,10),(20,61),
        (21,9),(21,3),(21,1),(21,48),(21,46),(21,35),
        (22,9),(22,3),(22,12),(22,20),(22,6),(22,47),(22,15),(22,5),(22,19),
        (23,9),(23,3),(23,1),(23,45),(23,31),(23,25),(23,49),(23,50),(23,17),(23,18),
        (24,9),(24,3),(24,31),(24,7),(24,51),(24,52),(24,53),(24,54),(24,55),(24,56),
        (25,9),(25,3),(25,1),(25,8),(25,57),(25,58),(25,59),
        (26,9),(26,3),(26,1),(26,8),(26,10),(26,60),(26,61),(26,62),(26,63),(26,64),
        (27,9),(27,3),(27,1),(27,8),(27,10),(27,65),(27,66),(27,67),(27,61),(27,63),
        (28,9),(28,3),(28,1),(28,68),(28,8),(28,10),(28,61),(28,19)
    ]
    cursor.executemany("INSERT OR IGNORE INTO plato_ingredientes (plato_id, ingrediente_id) VALUES (?,?)", plato_ingredientes)

    # Usuarios
    cursor.execute("INSERT OR IGNORE INTO usuarios (nombre_usuario) VALUES ('ana_g'), ('carlos_r')")
    cursor.execute("INSERT OR IGNORE INTO preferencias_ingredientes (usuario_id, ingrediente_id, puntuacion) VALUES (1,3,5)")
    cursor.execute("INSERT OR IGNORE INTO preferencias_ingredientes (usuario_id, ingrediente_id, puntuacion) VALUES (1,7,1)")
    cursor.execute("INSERT OR IGNORE INTO preferencias_ingredientes (usuario_id, ingrediente_id, puntuacion) VALUES (2,5,4)")
    cursor.execute("INSERT OR IGNORE INTO preferencias_ingredientes (usuario_id, ingrediente_id, puntuacion) VALUES (2,6,4)")

    print("Datos de ejemplo insertados correctamente.")

except sqlite3.IntegrityError:
    print("Los datos de ejemplo ya existían en la base de datos.")

#GUARDAR CAMBIOS Y CERRAR
conn.commit() 
conn.close()
print("Base de datos 'restaurante.db' finalizada y lista para usarse.")
