import requests
import random
import string

# 1. Autenticación y obtención del Token desde la API local
login_url = "http://library.demo.local/api/v1/loginViaBasic"
auth_resp = requests.post(login_url, auth=('cisco', 'Cisco123!'))

if auth_resp.status_code == 200:
    token = auth_resp.json().get("token")
    print("Token obtenido exitosamente.")
else:
    print(f"Error al autenticar: {auth_resp.status_code}")
    exit()

headers = {
    "X-API-KEY": token,
    "Content-Type": "application/json"
}

# Banco de datos para generación aleatoria
nombres = ["Gabriel", "Isabel", "Jorge", "Ana", "Carlos", "Sofia", "Lucia", "Mateo"]
apellidos = ["García", "Mistral", "Borges", "Vargas", "Rojas", "Neruda", "Allende"]
temas = ["Python", "Redes", "Ciberseguridad", "DevNet", "Linux", "Nube", "Automatización"]

books_url = "http://library.demo.local/api/v1/books"

print("\n--- Agregando 50 libros al azar ---")
# Se generan 50 libros utilizando IDs del 10 al 59
for i in range(10, 60):
    autor_random = f"{random.choice(nombres)}_{random.choice(apellidos)}"
    titulo_random = f"{random.choice(temas)} Avanzado Vol. {random.randint(1, 10)}"
    isbn_random = "".join(random.choices(string.digits, k=9))
    
    payload = {
        "id": i,
        "title": titulo_random,
        "author": autor_random,
        "isbn": isbn_random
    }
    
    r = requests.post(books_url, json=payload, headers=headers)
    if r.status_code == 200:
        print(f"Libro {i} agregado: '{titulo_random}' por {autor_random}")
    else:
        print(f"Error al agregar libro {i}: {r.status_code}")

# 2. Listar la totalidad de libros recorriendo las páginas
print("\n=================================================")
print("--- LISTADO COMPLETO DEL CATÁLOGO DE LA BIBLIOTECA ---")
print("=================================================")

todos_los_libros = []
page = 0

while True:
    res = requests.get(books_url, params={"includeISBN": "true", "page": page})
    if res.status_code == 200:
        datos = res.json()
        # Si la página devuelve una lista con elementos, los agregamos
        if isinstance(datos, list) and len(datos) > 0:
            todos_los_libros.extend(datos)
            page += 1
        else:
            break
    else:
        break

for libro in todos_los_libros:
    print(f"ID: {libro.get('id')} | Título: {libro.get('title')} | Autor: {libro.get('author')} | ISBN: {libro.get('isbn', 'N/A')}")

print(f"\nTotal de libros registrados en el catálogo: {len(todos_los_libros)}")

