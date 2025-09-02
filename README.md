# Vantage VPN - Native Desktop Client MVP

Vantage VPN is a prototype native Windows desktop application built in Python with PySide6. It simulates the core user flow of a commercial VPN client, including a mocked authentication screen and a dynamic server list with a simulated connection process.

This project was developed to meet a full-stack coding challenge, with a focus on applying prompt engineering, clean architecture, SOLID principles, and debugging.

## Features

- **Secure User Authentication (Mocked)**: A clean sign-in screen that simulates user validation.
- **Dynamic Node Discovery**: Fetches a list of VPN servers from a local mock API, complete with fluctuating latency to simulate live network conditions.
- **Search and Sort**: Instantly filter the server list by name/country or sort by ping and location.
- **Simulated Tunnel Connection**: A polished connection flow that transitions to a dedicated status screen, displaying connection time, the server's unique IP, and simulated upload/download speeds.
- **Native Windows Notifications**: Provides system-level feedback for connection and disconnection events.
- **Resizable UI**: A modern, resizable user interface built with a dark theme.

## Architecture Explanation

This application is built using a Clean Architecture approach, adapted for a desktop application. The primary goal is the Separation of Concerns, which makes the codebase modular, scalable, and highly testable.

The project is divided into three distinct layers:

### Presentation Layer (src/ui/)

- **Responsibility**: Manages all user interaction and UI state.
- **Technologies**: PySide6.

#### Main Window

This acts as a controller managing a QStackedWidget to switch between different screens (SignInWidget, NodeListWidget, ConnectedWidget). This layer is responsible for how the app looks and feels, but not for the core business logic.

### Domain Layer (src/models.py)

- **Responsibility**: Contains the core business objects of the application.

#### The VPNNode dataclass

This layer is the heart of the application and has no dependencies on the UI or data-fetching logic.

### Data Layer (src/api_client.py)

- **Responsibility**: Handles all data retrieval from external sources.
- **Technologies**: requests.

#### The fetch_nodes() function

This communicates with the Flask mock API. It is responsible for fetching raw data and converting it into the VPNNode objects defined in the Domain Layer.

This structure ensures that changes to the UI don't affect the data layer, and changes to the data source (e.g., moving to a real API) don't require any changes to the UI.

## Setup and Installation

Follow these steps to run the application locally.

### Prerequisites

- Python 3.8+
- pip and venv

### 1. Clone the Repository

```bash
git clone https://github.com/AlexBiobelemo/Project-Vantage
cd VantageVPN_Desktop
```

### 2. Create and Activate a Virtual Environment

**Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

The application requires two components to be running simultaneously in two separate terminals.

#### Terminal 1: Start the Mock API Server

```bash
python api.py
```

#### Terminal 2: Start the Desktop Client

```bash
python src
```

### 5. Running the Tests

To run the unit tests, use the pytest command from the root directory:

```bash
pytest
```

## AI Prompt Engineering & Decision Making

AI was used as a productivity tool for generating boilerplate code and shaping the project's direction.

### Initial Prompt (Project Direction)

"My time constraint is 1 day and I am using PyCharm. Which native platform (Android/Windows) would be the fastest to implement while being impressive?"

**Outcome**: This prompt led to the decision to use Python with PySide6, leveraging existing skills and tools to meet the tight deadline while still producing a native-feeling application.

### Core Logic Prompt (Data Fetching)

"Write a Python function using the requests library to fetch JSON data from a local API endpoint. It should handle connection errors gracefully and parse the successful JSON response into a list of VPNNode data classes."

**Outcome**: This generated the foundational api_client.py module, which was then integrated into the application.

### UI Boilerplate Prompt (Initial Screen)

"Create a simple login screen UI using PySide6. It needs a title, an email field, a secure password field, and a prominent 'Sign In' button. Use a QVBoxLayout."

**Outcome**: This produced the initial structure for signin_widget.py, which was then refactored to include signals and error handling.

## Major Bugs and Fixes

Several significant bugs were encountered and fixed during development, showcasing debugging skills on complex issues.

### Bug: ImportError: attempted relative import beyond top-level package

**Problem**: The test suite failed because pytest could not find the src module.

**Fix**: The initial fix involved creating a pyproject.toml file to configure the pythonpath. When this proved inconsistent, a more robust solution was implemented directly in the test file, which manually adds the src directory to sys.path. This guarantees that the tests can find the application modules in any environment.

### Bug: Cascade of Windows Notification Failures

**Problem**: The initial low-level pywin32 implementation for notifications was brittle, leading to a cascade of errors including Class already exists, Access is denied due to threading conflicts, and Unspecified error from the Windows shell.

**Fix**: After multiple attempts to patch the low-level API, the decision was made to replace the entire module with a high-level, maintained library (desktop-notifier). This demonstrates a key engineering principle: choosing the right tool for the job and prioritizing stability over a complex, custom implementation.

### Bug: asyncio Event Loop Errors

**Problem**: The desktop-notifier library is asynchronous, which initially caused RuntimeWarning: coroutine was never awaited and RuntimeError: Event loop is closed when called from our synchronous PySide6 application.

**Fix**: The final, professional-grade solution was to create a dedicated background daemon thread to run a persistent asyncio event loop for the entire application lifetime. The asyncio.run_coroutine_threadsafe function was then used to safely schedule notification tasks on this background loop from the main GUI thread, resolving all conflicts.

## Mock API Structure

The mock API is a simple Flask server that provides the VPN node data.

**Endpoint**: `GET /api/v1/nodes`

**Method**: GET

**Description**: Returns a JSON array of VPN node objects. To simulate a live environment, the latency_ms value for each node is slightly randomized on every API call.

**Success Response (200 OK)**:

```json
[
    {
        "id": "us-1",
        "name": "Eagle Server",
        "country": "United States",
        "latency_ms": 52,
        "ip_address": "104.26.10.188"
    },
    {
        "id": "ca-1",
        "name": "Maple Leaf",
        "country": "Canada",
        "latency_ms": 75,
        "ip_address": "142.126.146.1"
    }
]
```
```
