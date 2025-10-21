# Cliente del Juego de Lucha Pixel Art

Este repositorio contiene el código fuente del cliente para un juego de lucha multijugador con estética pixel art. El juego permite a los usuarios registrarse, iniciar sesión y participar en combates en tiempo real contra otros jugadores.

## Desarrollado por

- Cristian Galeano
- Leonardo Bermudez
- Said Acosta

### Características Principales

- **Autenticación de Usuarios:** Pantallas de registro e inicio de sesión para la gestión de cuentas.
- **Dashboard de Usuario:** Un panel central para ver otros jugadores conectados y lanzar desafíos de combate.
- **Combate Multijugador:** Sistema de combate en tiempo real utilizando comunicaciones por red (TCP para estado y UDP para posiciones).
- **Gráficos Pixel Art:** Todos los personajes, animaciones y escenarios siguen una cuidada estética retro.
- **Comunicaciones Seguras:** Uso de cifrado AES para proteger los mensajes intercambiados con el servidor.

### Tecnologías Utilizadas

- **Lenguaje:** Python 3
- **Librería Gráfica:** Pygame
- **Red:** Sockets (TCP/UDP)
- **Criptografía:** PyCryptodome (para AES)
- **Otros:** Requests, PyYAML

### Instalación y Ejecución

Sigue estos pasos para poner en marcha el cliente del juego en tu máquina local.

1.  **Clonar el repositorio:**
    ```bash
    # Reemplaza <URL_DEL_REPOSITORIO> con la URL real del repo
    git clone <URL_DEL_REPOSITORIO>
    cd pygame-stick-game/src
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # Crear el entorno
    python3 -m venv .venv

    # Activar en Linux/macOS
    source .venv/bin/activate

    # Activar en Windows
    # .\.venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    Se recomienda instalar las siguientes librerías usando pip.
    ```bash
    pip install pygame pycryptodome requests PyYAML
    ```

4.  **Ejecutar el juego:**
    Asegúrate de que el servidor del juego se esté ejecutando y luego lanza el cliente.
    ```bash
    python main.py
    ```
