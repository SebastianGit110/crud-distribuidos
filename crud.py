import mysql.connector
import sqlite3
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
from pydantic import BaseModel

app = FastAPI()

class ComidaMarina(BaseModel):
    nombre: str
    tipo: str
    precio: float
    disponible: int

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sea_food",
        port=3308
    )

@app.on_event("startup")
def startup_event():
    crear_tabla()

def crear_tabla():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comida_marina (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        tipo VARCHAR(50) NOT NULL,
        precio DECIMAL(10,2) NOT NULL,
        disponible TINYINT(1) NOT NULL
    );
    """)
    conexion.commit()
    cursor.close()
    conexion.close()

# Create

@app.post("/comida/")
def crear_comida(item: ComidaMarina):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO comida_marina (nombre, tipo, precio, disponible) VALUES (%s, %s, %s, %s)",
        (item.nombre, item.tipo, item.precio, item.disponible)
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return {"id": nuevo_id, "mensaje": "Comida creada con éxito"}

# Read all

@app.get("/comida/")
def listar_comida():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM comida_marina")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return {"comidas": filas}

# Read by id

@app.get("/comida/{comida_id}")
def obtener_comida(comida_id: int):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)  # <- Para que devuelva dicts en vez de tuplas
    cursor.execute("SELECT * FROM comida_marina WHERE id = %s", (comida_id,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Comida no encontrada")
    return {"comida": fila}

# Update

@app.put("/comida/{comida_id}")
def actualizar_comida(comida_id: int, item: ComidaMarina):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE comida_marina 
        SET nombre = %s, tipo = %s, precio = %s, disponible = %s 
        WHERE id = %s
        """,
        (item.nombre, item.tipo, item.precio, item.disponible, comida_id)
    )
    conexion.commit()
    cambios = cursor.rowcount
    cursor.close()
    conexion.close()

    if cambios == 0:
        raise HTTPException(status_code=404, detail="Comida no encontrada")
    return {"mensaje": "Comida actualizada con éxito"}

# Delete

@app.delete("/comida/{comida_id}")
def eliminar_comida(comida_id: int):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM comida_marina WHERE id = %s", (comida_id,))
    conexion.commit()
    cambios = cursor.rowcount
    cursor.close()
    conexion.close()
    if cambios == 0:
        raise HTTPException(status_code=404, detail="Comida no encontrada")
    return {"mensaje": "Comida eliminada con éxito"}
