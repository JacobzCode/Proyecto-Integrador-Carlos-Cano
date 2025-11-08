import csv
from typing import List, Dict

usuarios = {}  # Diccionario para almacenar usuarios

# Funciones para manejar usuarios
def registrar_usuario():
    print("=== Registro de Usuario ===")
    username = input("Ingresa un nombre de usuario: ")

    if username in usuarios:
        print("❌ El nombre de usuario ya existe. Intenta con otro.")
        return

    password = input("Ingresa una contraseña: ")
    confirm_password = input("Confirma tu contraseña: ")

    if password != confirm_password:
        print("❌ Las contraseñas no coinciden.")
        return

    usuarios[username] = {"password": password, "emociones": []}
    print(f"✅ Usuario '{username}' registrado exitosamente.\n")

def mostrar_usuarios():
    print("=== Lista de Usuarios Registrados ===")
    for username in usuarios:
        print(f"- {username}")
    print()

# Funciones para manejar encuestas emocionales
def registrar_emocion():
    print("=== Registro de Emoción ===")
    username = input("Ingresa tu nombre de usuario: ")

    if username not in usuarios:
        print("❌ El usuario no está registrado. Regístrate primero.")
        return

    emocion = input("¿Cómo te sientes hoy? (Ejemplo: feliz, triste, ansioso): ")
    descripcion = input("Describe brevemente por qué te sientes así: ")

    usuarios[username]["emociones"].append({"emocion": emocion, "descripcion": descripcion})
    print(f"✅ Emoción registrada para el usuario '{username}'.\n")

def mostrar_emociones():
    print("=== Emociones Registradas ===")
    for username, data in usuarios.items():
        print(f"Usuario: {username}")
        for emocion in data["emociones"]:
            print(f"  - Emoción: {emocion['emocion']}, Descripción: {emocion['descripcion']}")
    print()

# Funciones para manejar archivos CSV
def read_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and returns a list of dictionaries.

    :param file_path: Path to the CSV file.
    :return: List of rows as dictionaries.
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(file_path: str, data: List[Dict[str, str]], fieldnames: List[str]) -> None:
    """
    Writes a list of dictionaries to a CSV file.

    :param file_path: Path to the CSV file.
    :param data: List of rows as dictionaries.
    :param fieldnames: List of field names (keys) for the CSV file.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        print("=== Menú Principal ===")
        print("1. Registrar Usuario")
        print("2. Mostrar Usuarios")
        print("3. Registrar Emoción")
        print("4. Mostrar Emociones")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            registrar_emocion()
        elif opcion == "4":
            mostrar_emociones()
        elif opcion == "5":
            print("👋 Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")