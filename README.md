# 🏫 Alpha V2 — Modern School Management System

_La evolución moderna de una plataforma de gestión escolar. Refactorización completa de una arquitectura monolítica legacy a una arquitectura desacoplada y escalable._

![React](https://img.shields.io/badge/React_18-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-In_Development-yellow?style=flat-square)

## About the Project

**Alpha V2** no es solo una actualización de código; es una reingeniería total. El objetivo fue tomar un proyecto estudiantil ("Legacy") y transformarlo en un producto profesional, aplicando patrones de diseño de software y separando responsabilidades.

El resultado es una aplicación Full Stack robusta que permite la administración de usuarios, calificaciones y cursos, lista para escalar.

## 🤖 Metodología "Vibe Coding" (AI-Augmented Engineering)

Este proyecto es una demostración de eficiencia en ingeniería de software moderna. Utilicé un flujo de trabajo **Human-in-the-Loop**, actuando como **Technical Lead** para orquestar agentes de IA (Copilot/Gemini), maximizando la productividad sin sacrificar la calidad ni el control arquitectónico.

**Mi Rol (Arquitectura & Ingeniería) vs. IA (Generación):**

La IA se utilizó estrictamente como un motor de generación de código y documentación, bajo mi supervisión directa y corrección constante.

- **Dirección Técnica:** Diseño manual de la arquitectura desacoplada (Frontend/Backend) y selección del stack tecnológico. La IA ejecutó las tareas repetitivas, pero yo definí la estructura de carpetas y los patrones de diseño (Factory Pattern, Services Layer).
- **Prompt Engineering Avanzado:** Uso de técnicas de prompting secuencial y contextual para guiar al agente de Copilot en refactorizaciones complejas, asegurando que el código generado cumpliera con estándares estrictos de limpieza y escalabilidad.
- **Resolución de Conflictos Críticos:** Intervención manual para solucionar problemas que la IA no pudo resolver, específicamente conflictos de entorno en Windows/PowerShell, dependencias circulares en Python y la configuración de seguridad (CORS).
- **Seguridad y Best Practices:** Implementación manual de estrategias de seguridad, gestión correcta de variables de entorno (`.env`) y saneamiento del repositorio para asegurar un historial de Git limpio y profesional.

### Fases de Refactorización Ejecutadas

1. **Fase 1 - Arquitectura Backend:** Transformación de un `app.py` monolítico a una estructura modular con **Factory Pattern** y **Blueprints**.
2. **Fase 2 - Desacoplamiento:** Extracción de lógica de negocio desde las rutas hacia una **Capa de Servicios (Service Layer)** para mantener los controladores limpios (Thin Controllers).
3. **Fase 3 - Estandarización Frontend:** Migración de componentes desordenados a una arquitectura **Feature-First**, centralizando el cliente API y creando Custom Hooks.

## Tech Stack

- **Frontend:** React 19 + Vite (Arquitectura Feature-First para escalabilidad).
- **Backend:** Python 3 + Flask (Estructurado con Blueprints y Servicios).
- **Base de Datos:**
  - _Dev:_ SQLite (Configuración local rápida).
  - _Prod:_ PostgreSQL Ready (Compatible vía SQLAlchemy).
- **Estilos:** Bootstrap 5 (Integrado vía NPM).
- **Gestión de Dependencias:** Pipenv (Entornos virtuales Python) & NPM (Node packages).

## Project Structure

```text
alpha/
├── client/                 # Frontend (React + Vite)
│   ├── src/
│   │   ├── common/         # Componentes UI reutilizables y hooks globales
│   │   ├── features/       # Módulos de negocio (Auth, Teachers, Students)
│   │   └── api/            # Cliente HTTP centralizado (Axios/Fetch wrapper)
├── src/                    # Backend (Flask)
│   ├── app/
│   │   ├── api/            # Blueprints (Definición de rutas)
│   │   ├── services/       # Lógica de Negocio Pura (Service Layer)
│   │   └── models.py       # Modelos SQLAlchemy (Tablas)
│   └── app.py              # Configuración (Factory Pattern)
└── Pipfile                 # Dependencias Python (Lockfile)
```

## Getting Started

Sigue estos pasos para levantar el entorno de desarrollo localmente.

### Prerequisites

-Node.js (v18+)
-Python (v3.10+)
-Pipenv (`pip install pipenv`)

### 1. Configuración del Backend (Flask)

```bash
# 1. Instalar dependencias y entorno virtual
pipenv install

# 2. Activar el entorno
pipenv shell

# 3. Crear la base de datos local (SQLite)
flask shell
>>> from src.app import app
>>> from src.models import db
>>> with app.app_context(): db.create_all()
>>> exit()

# 4. Iniciar el servidor
flask run
# El backend correrá en http://127.0.0.1:5000
```

### 2. Configuración del Frontend (React)

En una nueva terminal:

```bash
cd client

# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desarrollo
npm run dev
# El frontend correrá en http://localhost:3000
```

## Author

Designed and developed with ☕ by **Alejandro Guzmán** [@alguzdev](https://alguzdev.vercel.app/)
