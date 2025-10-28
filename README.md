# ATM Banking Application - Python

## Table of Contents
- [ATM Banking Application - Python](#atm-banking-application---python)
  - [Table of Contents](#table-of-contents)
  - [OVERVIEW](#overview)
    - [Under the hood of ATM software](#under-the-hood-of-atm-software)
      - [What is an ATM?](#what-is-an-atm)
      - [ATM hardware](#atm-hardware)
      - [Who is running this zoo?](#who-is-running-this-zoo)
      - [For card reader:](#for-card-reader)
      - [Banking application](#banking-application)
      - [How does it work](#how-does-it-work)
      - [Example configuration of a typical state A:](#example-configuration-of-a-typical-state-a)
      - [The rest of the states are arranged in a similar way:](#the-rest-of-the-states-are-arranged-in-a-similar-way)
      - [Now about screens](#now-about-screens)
  - [WEB INTERFACE ARCHITECTURE](#web-interface-architecture)
    - [Controller Layer (`controllers/default.js`)](#controller-layer-controllersdefaultjs)
      - [Key Components:](#key-components)
      - [WebSocket Functionality:](#websocket-functionality)
      - [Data Flow:](#data-flow)
      - [Security Features:](#security-features)
    - [Views Layer (views/)](#views-layer-views)
      - [Customization tips](#customization-tips)
    - [File Structure:](#file-structure)
    - [Usage:](#usage)
  - [TESTING](#testing)
  - [UNIT TESTING](#unit-testing)

## OVERVIEW

### Under the hood of ATM software

We read numerous articles on GT and Habré about bank cards and ATMs, and We decided to make our contribution. Below, I will try to talk about how the ATM is arranged in terms of software.

#### What is an ATM?
Any ATM is essentially a computer with connected peripherals, an equipment manager and the actual banking application that manages the entire economy. All decisions on the issuance of money are made by the server. The ATM only collects information from the client and transmits it to the server.

#### ATM hardware
The minimum set of ATM hardware includes:
- Card reader, for reading a customer's card
- Pin pad, for entering a pin code and other information, such as payment/withdrawal amounts
- Function keys on the sides (4 + 4) or a touch screen
- Money dispenser
- Various sensors, backlight

#### Who is running this zoo?
To unify hardware and software, the CEN/XFS standard (eXtension For Financial Services) was created. It describes a client-server architecture with a hardware manager and service providers (device drivers). All interaction with the equipment occurs through the XFS Manager API.

#### For card reader:
- WFS_CMD_IDC_RETAIN_CARD (card capture)
- WFS_CMD_IDC_READ_TRACK (read tracks)

There are several implementations of XFS managers (including open source ones) written in C++ and Java.

#### Banking application
The banking app is what you see on the screen when you approach the device. It collects data from the user, sends it to the host (server), and executes the response. There are industry protocols (NDC/DDC) for communication.

#### How does it work
At any given time, the ATM is in one of the following operating modes:
- Power Up- Loading
- Offline - No connection to the server
- Supervisor - a collector or service engineer works
- Out of service - the ATM does not work
- In service - the main mode of operation

In service mode, the ATM is in one of the states (001-999), each with a description string.

#### Example configuration of a typical state A:
```
000 A001001011008004002001104
```
- 000 - state number
- A - state type (Card read state)
- 001 - Screen number
- 001 - state number to go to in case of successful card reading
- 011 - state number to go to in case of map reading errors
- 008, 004, 002 - read conditions
- 001 - card return condition
- 104 - transition state if the card is unknown to the bank

#### The rest of the states are arranged in a similar way:
- States for reading the sum from the keyboard
- States for reading a PIN code
- States for checking the entered data
- States for selecting using the side keys
- States for resetting and presetting buffers

The application eventually interacts with the host (server) to process transactions.

#### Now about screens
The ATM screen is a field of 32x16 cells. It can contain both graphic and textual information. Screens are referenced by number.


## WEB INTERFACE ARCHITECTURE

This ATM Banking Application includes a web-based interface that provides terminal access to the Python application through a browser. The architecture consists of:

### Controller Layer (`controllers/default.js`)

The main controller handles the web interface and terminal integration:

#### Key Components:
- **WebSocket Connection**: Establishes real-time communication between the web client and the ATM application
- **Pseudo-Terminal Integration**: Uses `node-pty` to spawn Python processes and manage terminal sessions
- **Credential Management**: Handles initialization of credentials from environment variables

#### WebSocket Functionality:
- **Terminal Spawning**: Each client connection spawns a new pseudo-terminal running `python3 run.py`
- **Real-time Communication**: Forwards terminal output to clients and user input to the terminal
- **Process Management**: Handles terminal process lifecycle including cleanup on disconnection
- **Terminal Configuration**: 
  - Terminal type: `xterm-color` (for color support)
  - Dimensions: 80 columns × 24 rows
  - Environment: Inherits from host system

#### Data Flow:
1. Client connects via WebSocket to `/` route
2. Server spawns Python terminal process (`run.py`)
3. Terminal output is forwarded to client in real-time
4. User input from web interface is sent to terminal
5. Process cleanup occurs when client disconnects

#### Security Features:
- Automatic session cleanup on disconnection
- Force termination of orphaned processes
- Environment variable-based credential initialization

### Views Layer (views/)
- layout.html
  - Base HTML layout loaded by the template engine.
  - Includes jQuery, xterm.js, and the xterm attach addon via CDN.
  - Defines global styles (including xterm defaults), base page styling, and the ATM background.
  - Renders page content at the @{body} placeholder inside <main id="main-container">.
- index.html
  - Renders the Run Program button and the #terminal container.
  - Initializes xterm with 80x24 size, prints a startup message, opens a WebSocket to the server root (/), and attaches the terminal to the socket.
  - Sets focus to the terminal input after load.

#### Customization tips
- Terminal size: change cols/rows in index.html Terminal({...}).
- Page/ATM background and styles: edit CSS in layout.html (body, #main-container, .xterm).
- Library versions: update the CDN URLs in layout.html.

### File Structure:
```
controllers/
  └── default.js     # Main WebSocket controller for terminal integration
views/
  ├── layout.html    # Base layout + xterm includes/styles
  └── index.html     # Terminal UI + WebSocket client bootstrap
run.py              # Main Python ATM application entry point
creds.json          # Credentials file (generated from environment)
```

### Usage:
The web interface allows users to interact with the ATM Banking Application through a browser-based terminal, providing the full ATM experience without requiring direct Python execution on the client machine.

## TESTING


## UNIT TESTING

Unit tests are written using Python's built-in `unittest` module. To create and run unit tests for this project:

1. Create a new file, for example, `unittest.py` in the project directory.
2. Add test cases for your classes and functions. Example for the `card` class:

```python
import unittest

```

3. Run your tests from the terminal:
```
python unittest.py
```

This will run all the test cases and show the results. You can create similar test files for other modules and functions.
