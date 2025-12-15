from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'una_clave_secreta_fuerte')

# URL base de la API cargada desde .env
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:5001')
BOOKS_API_URL = f"{API_BASE_URL}/books"

# --- Funciones de Comunicación HTTP (Cliente de la API) ---

def api_request(method, url, data=None):
    """Manejador genérico de solicitudes a la API."""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=5)
        else:
            raise ValueError("Método HTTP no soportado")

        # Manejo de errores de red o códigos HTTP 4xx/5xx
        response.raise_for_status()
        
        # Intenta decodificar JSON, si falla, retorna texto o None
        if response.content:
            return response.json()
        return {} # 200 o 204 sin contenido
        
    except requests.exceptions.HTTPError as e:
        # Esto captura 404, 400, 500 de la API
        error_message = f"Error de la API ({response.status_code}): {response.text}"
        flash(error_message, 'danger')
        return None
    except requests.exceptions.RequestException as e:
        # Esto captura errores de red, conexión, timeout
        flash(f"Error de conexión con la API: {e}", 'danger')
        return None
    except ValueError as e:
        flash(f"Error interno en la solicitud: {e}", 'danger')
        return None

# --- Vistas de la Aplicación (Consumo de la API) ---

@app.route('/')
def index():
    """Obtener y mostrar todos los libros."""
    books_data = api_request('GET', BOOKS_API_URL)
    
    if books_data is None:
        # La función api_request ya flashea el error
        books = []
    else:
        books = books_data
        
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """Agregar un nuevo libro."""
    if request.method == 'POST':
        book_data = {
            'title': request.form['title'],
            'author': request.form['author'],
            'year': int(request.form['year'])
        }
        
        response_data = api_request('POST', BOOKS_API_URL, data=book_data)
        
        if response_data:
            flash(f"Libro '{book_data['title']}' agregado con éxito.", 'success')
            return redirect(url_for('index'))
            
        # Si falla, api_request ya flashea el error y redirigimos de vuelta al formulario
        return redirect(url_for('add_book'))

    return render_template('book_form.html', title="Agregar Libro", book={})

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """Editar un libro existente."""
    url = f"{BOOKS_API_URL}/{book_id}"
    
    if request.method == 'GET':
        book = api_request('GET', url)
        if book is None:
            # Error ya flasheado (ej. 404)
            return redirect(url_for('index'))
        return render_template('book_form.html', title="Editar Libro", book=book)

    elif request.method == 'POST':
        book_data = {
            'title': request.form['title'],
            'author': request.form['author'],
            'year': int(request.form['year'])
        }
        
        response_data = api_request('PUT', url, data=book_data)
        
        if response_data:
            flash(f"Libro '{book_data['title']}' actualizado con éxito.", 'success')
            return redirect(url_for('index'))

        # Si falla, volvemos a intentar la edición, cargando los datos originales (o None)
        return redirect(url_for('edit_book', book_id=book_id))

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book_view(book_id):
    """Eliminar un libro."""
    url = f"{BOOKS_API_URL}/{book_id}"
    
    response_data = api_request('DELETE', url)
    
    if response_data is not None:
        flash(f"Libro con ID {book_id} eliminado correctamente.", 'success')
    # Si falla (404 o error de red), api_request ya flashea el error

    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('CLIENT_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
