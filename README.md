# API

# Estructura

## /controllers

**Propósito** Lógica

En esta carpeta se definirán las funciones que se encargaran de ejecutar acciones concretas como: obtener datos, hacer cálculos, validar condiciones, enviar correos, etc.

## /database

**Propósito** Conexión DB

Conexión y configuración de la base de datos

## /models

**Propósito** Definir las tablas de la Base de Datos

Con SQLAlchemy se definirán las clases que representan las tablas

## /routers

**Propósito** Agrupar las rutas `endpoints`

En esta carpeta se definen las rutas HTTP de la API, es decir, las funciones que responden a las peticiones GET, POST, PUT, DELETE, etc.

## /schemas

**Propósito** Validar y estructurar los datos con Pydantic

Son modelos de datos que se definen con Pydantic usados para validar los datos que llegan a la API, formatear respuestas, documentar la API, etc.
