from flask import Flask, jsonify, request
from data_store import get_all_books, get_book_by_id, add_new_book, update_book, delete_book
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Función de validación simple
def validate_book_data(data):
    if not data or 'title' not in data or 'author' not in data or 'year' not in data:
        return False
    try:
        data['year'] = int(data['year'])
        if data['year'] <= 0: return False
    except ValueError:
        return False
    return True

# --- Endpoints ---

@app.route('/books', methods=['GET'])
def list_books():
    """GET /books -> Obtener la lista de libros."""
    books = get_all_books()
    return jsonify(books), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """GET /books/<id> -> Obtener un libro específico."""
    book = get_book_by_id(book_id)
    if book:
        return jsonify(book), 200
    return jsonify({"message": f"Libro con ID {book_id} no encontrado"}), 404

@app.route('/books', methods=['POST'])
def create_book():
    """POST /books -> Agregar un nuevo libro."""
    data = request.get_json()
    if not validate_book_data(data):
        return jsonify({"message": "Datos de libro incompletos o inválidos."}), 400
    
    new_book = add_new_book(data)
    # Devuelve 201 Created y la ubicación del nuevo recurso
    return jsonify(new_book), 201, {'Location': f'/books/{new_book["id"]}'}

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book_endpoint(book_id):
    """PUT /books/<id> -> Actualizar la información de un libro."""
    book = get_book_by_id(book_id)
    if not book:
        return jsonify({"message": f"Libro con ID {book_id} no encontrado"}), 404

    data = request.get_json()
    # Para PUT, verificamos que los campos obligatorios estén en el request body
    if not validate_book_data(data):
        return jsonify({"message": "Datos de libro incompletos o inválidos para actualización."}), 400

    updated_book = update_book(book_id, data)
    return jsonify(updated_book), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book_endpoint(book_id):
    """DELETE /books/<id> -> Eliminar un libro."""
    if delete_book(book_id):
        return jsonify({"message": f"Libro con ID {book_id} eliminado"}), 200
    return jsonify({"message": f"Libro con ID {book_id} no encontrado"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('API_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
