# Stickman Capstone Client

This is the client application for the Stickman Capstone project. It provides a graphical interface for users to interact with the game server.

## Features

*   User Authentication (Login/Register)
*   Dashboard
*   Combat Screen
*   Code Screen
*   Game History
*   Secure communication using AES encryption over TCP and UDP.

## Prerequisites

Before running the client, ensure you have the following:

*   **Python:** A Python installation on your system.
*   **Game Server:** The corresponding game server must be running and accessible at `136.112.137.217:5000` (for TCP) and `136.112.137.217:9876` (for UDP). The server is responsible for providing the necessary AES encryption keys upon connection.

## Setup and Installation

Follow these steps to set up and run the client:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd stickman-capstone-client
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install pygame pycryptodome
    ```

5.  **Ensure AES Keys are Available:**
    The client expects an `aes_keys.json` file in the `src/` directory, which is initially populated by the server during the first connection. If this file is missing or corrupted, the client might not be able to establish secure communication. The server should provide the initial keys.

## Running the Client

Once the setup is complete and the game server is running, you can start the client:

```bash
python src/main.py
```

## Project Structure

The project is organized into several modules, each handling a specific part of the application:

*   `src/main.py`: The main entry point of the application.
*   `src/login_screen/`: Handles user login.
*   `src/register_screen/`: Handles user registration.
*   `src/combat_screen/`: Manages the combat interface.
*   `src/code_screen/`: For code-related interactions.
*   `src/dashboard/`: Displays user dashboard information.
*   `src/menu/`: The main menu.
*   `src/history/`: Displays game history.
*   `src/tcp_listener.py`: Manages incoming TCP messages from the server.
*   `src/udp_service/`: Handles UDP communication for real-time data.
*   `src/encryptAES/`: Contains utilities for AES encryption and decryption.
*   `src/static/`: Stores static assets like images and sounds.