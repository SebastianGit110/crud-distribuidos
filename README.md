# 🍤 API de Comida Marina - FastAPI + MySQL

Esta es una API RESTful desarrollada con **FastAPI** y **MySQL** para gestionar un catálogo de comidas marinas.  
Implementa un **CRUD completo** (Crear, Leer, Actualizar y Eliminar).

---

## 🚀 Tecnologías usadas
- [FastAPI](https://fastapi.tiangolo.com/) - Framework para construir APIs rápidas.
- [MySQL](https://www.mysql.com/) - Base de datos relacional.
- [Pydantic](https://docs.pydantic.dev/) - Validación de datos.
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para correr la API.

---

## 📂 Estructura de la Base de Datos

La API crea automáticamente la tabla `comida_marina` al iniciar si no existe:

```sql
CREATE TABLE IF NOT EXISTS comida_marina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    disponible TINYINT(1) NOT NULL
);

## Endpoints

### 1. Crear comida
**POST** `/comida/`

Crea un nuevo registro en la tabla `comida_marina`.

#### Request Body (JSON)
```json
{
  "nombre": "Ceviche",
  "tipo": "Entrada",
  "precio": 25000,
  "disponible": true
}

