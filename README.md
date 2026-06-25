# Sokoban Python Edition

[![GitHub Actions Status](https://img.shields.io/github/actions/workflow/status/Valentino-Carmona/Sokoban/ci.yml?branch=main&label=Build%20Status&logo=github)](https://github.com/Valentino-Carmona/Sokoban/actions)
[![Tests Status](https://img.shields.io/github/actions/workflow/status/Valentino-Carmona/Sokoban/ci.yml?branch=main&label=Tests&logo=pytest)](https://github.com/Valentino-Carmona/Sokoban/actions)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](#)


> [!NOTE]
> **Estado del Proyecto:** Esta versión en Python constituye el **MVP (Producto Mínimo Viable) final** presentado al cliente para validar la experiencia de juego. Representa el juego prácticamente terminado en cuanto a su lógica y mecánicas principales, desarrollo que sirvió como base para ser portado posteriormente y funcionar en la página web del cliente.

¡Bienvenido a **Sokoban Python Edition**! Esta es una versión moderna, ligera y robusta del clásico juego de ingenio japonés. Diseñado con un enfoque limpio y una arquitectura de software desacoplada, este proyecto ofrece una experiencia de juego fluida, intuitiva y con herramientas avanzadas para resolver acertijos como base de desarrollo.

## 🎮 ¿De qué se trata el juego?

**Sokoban** (que significa "guardián de almacén" en japonés) es un juego de puzles de transporte. 

El jugador encarna a un operario dentro de un almacén representado por una cuadrícula. El objetivo es simple pero desafiante: **empujar todas las cajas distribuidas por el mapa hasta colocarlas sobre los puntos de destino designados**.

### Reglas Clave (Mecánica de Gameplay):
* **Fuerza bruta limitada**: El personaje solo puede *empujar* las cajas. No es posible tirar de ellas (arrastrarlas).
* **Límite de empuje**: Solo se puede empujar **una caja a la vez**. Intentar empujar una fila de dos o más cajas no tendrá efecto.
* **Laberinto de obstáculos**: Las paredes delimitan el mapa, por lo que un mal movimiento puede arrinconar una caja contra una esquina o contra otra caja, haciéndola imposible de mover y bloqueando el nivel. ¡La planificación es clave!

---

## ✨ Características Especiales y Jugabilidad

Este motor de Sokoban ha sido desarrollado para brindar una experiencia de usuario sumamente cómoda e intuitiva, agregando características premium al clásico juego:

### 🕒 Historial Inteligente de Movimientos (Undo / Redo)
¿Cometiste un error o arrinconaste una caja por accidente? No es necesario reiniciar el nivel. El juego cuenta con un sistema de pila para **Deshacer** y **Rehacer** tus movimientos de forma ilimitada, permitiéndote retroceder paso a paso para corregir tu estrategia.

### 🧠 Motor de Resolución Automática (Pistas con Backtracking)
Si te encuentras atascado en un nivel especialmente complejo, el motor integra un resolvedor inteligente basado en **Backtracking**. Al presionar el botón de pista, el algoritmo calcula en tiempo real la solución óptima desde tu estado actual y realiza el siguiente movimiento sugerido para guiarte hacia la victoria.

### 📐 Pantalla Adaptativa Dinámica
El tablero gráfico se adapta y redimensiona de forma automática según la escala y dimensiones del nivel cargado, asegurando siempre una visualización perfecta y cómoda sin importar el tamaño del mapa.

### ⚙️ Controles Personalizables
Los controles del juego están mapeados mediante un archivo de configuración externo (`teclas.txt`), permitiéndote adaptar la jugabilidad a tus preferencias fácilmente.

---

## 🕹️ Controles por Defecto

El juego cuenta con un esquema de control intuitivo y redundante para adaptarse a cualquier estilo de juego:

| Tecla | Acción | Descripción |
| :--- | :--- | :--- |
| **⬆️** / **W** | Mover al Norte | Mueve al personaje hacia arriba. |
| **⬇️** / **S** | Mover al Sur | Mueve al personaje hacia abajo. |
| **⬅️** / **A** | Mover al Oeste | Mueve al personaje hacia la izquierda. |
| **➡️** / **D** | Mover al Este | Mueve al personaje hacia la derecha. |
| **`1`** | Deshacer | Retrocede un movimiento en el historial (Undo). |
| **`2`** | Rehacer | Re-aplica el último movimiento deshecho (Redo). |
| **`3`** | Pistas / Resolver | Activa el asistente inteligente para darte el siguiente paso sugerido. |
| **`R`** | Reiniciar | Reinicia el nivel actual al estado inicial en un instante. |
| **`Esc`** | Salir | Cierra el juego de forma segura. |

---

## 🎨 Aspecto Visual

El proyecto cuenta con un conjunto de recursos visuales retro de alta fidelidad que representan de forma clara los distintos elementos en pantalla:
* 👷 **El Personaje**: Cambia visualmente al encontrarse sobre un punto de objetivo.
* 📦 **Las Cajas**: Cambian de color/aspecto cuando son colocadas correctamente sobre un objetivo para dar un feedback visual inmediato al jugador.
* 🎯 **Los Objetivos**: Marcas en el suelo que indican dónde deben ser depositadas las cajas.
* 🧱 **Las Paredes**: Bloques sólidos que definen los límites del almacén.

---

## 🏗️ Arquitectura y Estructura del Proyecto

El proyecto está diseñado bajo un modelo de arquitectura **Cliente-Servidor (MVP Web)** que sigue el principio de separación de responsabilidades (*Separation of Concerns*). Se divide en dos capas principales:

### 1. Backend (Python)
Toda la lógica pura del juego reside en el directorio `backend/`. Esta separación clara favorece el principio de responsabilidad única.
* **`backend/src/soko.py`**: Es el motor puro del Sokoban. Gestiona el estado de la grilla, reglas de colisión y el movimiento de cajas/jugadores sin ninguna dependencia externa.
* **`backend/src/clase.py`**: Implementa estructuras de datos abstractas genéricas (`Pila` y `Cola`) que construyen el cimiento para el historial de movimientos y los algoritmos de búsqueda (Backtracking).
* **`backend/src/data/`**: Carpeta designada para archivos de configuración y mapas (`niveles.txt`, `teclas.txt`). Aislar los datos del código fuente es una buena práctica clave de estructuración de repositorios modernos.
* **`backend/src/app.py`**: Es el puente de comunicación utilizando el micro-framework **Flask**. Expone una API REST con endpoints como `/api/start` y `/api/move` para recibir comandos del navegador y devolver el nuevo estado de la grilla, manejando la sesión en la memoria del servidor.

### 2. Frontend Web (HTML / CSS / JS)
La capa de presentación ha sido aislada en su propio entorno dentro del directorio `frontend/src/`.
* **`index.html`**: Provee el marco esquelético y la estructura semántica de la aplicación.
* **`style.css`**: Aporta todo el valor estético moderno, con uso de variables CSS para el esquema de colores, efectos visuales tipo glassmorphism/sombras y un sistema de grillas dinámicas e imágenes escalables que reemplazan la anterior ventana estática.
* **`script.js`**: Maneja la interacción del usuario. Escucha de forma asíncrona los eventos del teclado, los empaqueta en JSON hacia la API y luego se encarga del renderizado de imágenes (`img/`) sobre el tablero del cliente basándose estrictamente en lo que dictamina el backend.

### 🛡️ Buenas Prácticas de Ingeniería Implementadas
* **Estructura Fullstack Segregada**: Dividir el proyecto físicamente en `frontend/` y `backend/` ayuda a encapsular dependencias (como se ve en `backend/requirements.txt`), facilita futuros despliegues desacoplados, simplifica la integración continua y hace el proyecto más amigable para desarrolladores habituados a arquitecturas web modernas.
* **Desacoplamiento Extremo**: El frontend web desconoce por completo las reglas lógicas para completar el nivel o las colisiones. De forma similar, la capa en Python (`soko.py`) no invoca bibliotecas gráficas y retorna tipos de datos primitivos nativos de Python.
* **Diseño Orientado al MVP (Minimum Viable Project)**: La adopción de Flask evitó reescribir toda la aplicación. Permite reutilizar el 100% de la base de código original de consola/escritorio transformándola en una aplicación para web con una capa mínima de re-enrutamiento.
* **Alta Fiabilidad vía Testing Automatizado**: En el directorio `backend/tests/unit/`, el proyecto incorpora pruebas automatizadas con herramientas de la industria (`pytest`). Valida desde la integridad estructural interna de la Pila, los bordes en el mapa del Sokoban, y el propio API HTTP final de la aplicación en Python. Todo esto respaldado por un reporte de trazabilidad que garantiza un **estado mayor al 90% en la cobertura del código**, limitando severamente la introducción de bugs (regresiones) a futuro.

---

## 🚀 Instalación y Ejecución

Guía paso a paso para clonar, instalar y correr el proyecto, además de ejecutar sus pruebas y ver el reporte de cobertura.

### 📥 1. Descargar el Proyecto

Si aún no tienes el código en tu máquina, primero descárgalo:

1. **Clona el repositorio** desde GitHub:
   ```bash
   git clone https://github.com/Valentino-Carmona/Sokoban.git
   ```
2. **Navega al directorio del juego**:
   ```bash
   cd Sokoban
   ```

---

### 🎮 2. Instalación y Ejecución (Elige tu Opción)

Tienes dos alternativas para preparar y ejecutar el juego, dependiendo de tus herramientas y nivel de experiencia.

#### 🐳 Opción A: Usando Docker (Recomendado)

Esta es la forma más rápida y robusta. No necesitas configurar entornos virtuales ni instalar Python en tu máquina; Docker aislará todo el ambiente por ti.

1. **Construye y levanta el contenedor** desde la consola:
   ```bash
   docker compose up --build
   ```

#### 🐍 Opción B: Usando Python (Entorno Virtual)

Si no tienes Docker o prefieres una instalación local, puedes usar Python. Esta opcion sirve para no instalar dependencias en tu maquina.

1. **Crea y activa un entorno virtual**:
   * En **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * En **macOS/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. **Instala las dependencias necesarias**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Inicia el servidor Flask**:
   ```bash
   cd backend/src
   python app.py
   ```
---

### 🌐 3. ¡A Jugar!

Una vez que el servidor reporte que está corriendo (ya sea a través de Docker o de tu consola de Python):

1. **Abre tu navegador web** e ingresa a la siguiente dirección:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. ¡Listo! Ya puedes disfrutar de la experiencia Sokoban MVP en tu navegador con soporte completo para todas las mecánicas.

---

### 🧪 3. Correr las Pruebas y Observar Cobertura

El proyecto cuenta con un conjunto robusto de pruebas automatizadas escritas en `pytest`.

* **Correr las pruebas unitarias e integración**:
  * En **Windows** (PowerShell):
    ```powershell
    $env:PYTHONPATH="backend/src"; python -m pytest backend/tests/
    ```
  * En **Linux/macOS**:
    ```bash
    PYTHONPATH=backend/src python -m pytest backend/tests/
    ```
  *(O simplemente `pytest` con el entorno virtual activo)*

* **Correr las pruebas y ver la cobertura en consola**:
  Para ver la cobertura de cada archivo y saber qué líneas específicas faltan probar:
  ```bash
  python -m pytest --cov=. --cov-report=term-missing
  ```