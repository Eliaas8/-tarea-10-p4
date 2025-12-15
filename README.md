#  Biblioteca Personal Desacoplada: Cliente/API REST

Este proyecto implementa una arquitectura de aplicación distribuida, separando la lógica de datos (Backend API RESTful) de la lógica de presentación y negocio (Frontend Cliente Flask).

##  Arquitectura del Proyecto

| Servicio | Tecnología | Puerto por Defecto | Responsabilidad |
| :--- | :--- | :--- | :--- |
| **API Backend** | Flask | 5001 | Gestión de datos CRUD de libros. Devuelve JSON. |
| **Cliente Frontend** | Flask + Requests | 5000 | Renderiza vistas HTML, maneja la interfaz y consume la API Backend a través de HTTP. |

##  Cómo Ejecutar

### 1. Requisitos

* Python 3.x
* Instalar las dependencias en cada proyecto.

### 2. Configuración y Ejecución de la API Backend (Puerto 5001)

```bash
# Navegar a la carpeta api_backend
pip install -r requirements.txt
python app.py
