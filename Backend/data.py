BOOKS = {
    1: {"title": "Cien años de soledad", "author": "Gabriel García Márquez", "year": 1967},
    2: {"title": "Don Quijote de la Mancha", "author": "Miguel de Cervantes", "year": 1605},
}
NEXT_ID = 3

def get_all_books():
    """Retorna todos los libros."""
    return list(BOOKS.values())

def get_book_by_id(book_id):
    """Retorna un libro por ID."""
    return BOOKS.get(book_id)

def add_new_book(data):
    """Agrega un nuevo libro y le asigna un ID."""
    global NEXT_ID
    book_id = NEXT_ID
    BOOKS[book_id] = data
    BOOKS[book_id]['id'] = book_id # Añade el ID al objeto de retorno
    NEXT_ID += 1
    return BOOKS[book_id]

def update_book(book_id, data):
    """Actualiza la información de un libro existente."""
    if book_id in BOOKS:
        BOOKS[book_id].update(data)
        BOOKS[book_id]['id'] = book_id
        return BOOKS[book_id]
    return None

def delete_book(book_id):
    """Elimina un libro por ID."""
    if book_id in BOOKS:
        del BOOKS[book_id]
        return True
    return False
