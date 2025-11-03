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
    - [Usage (Localhost)](#usage-localhost)
    - [Deploy on Render (Quick Guide)](#deploy-on-render-quick-guide)
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

![Screenshot 38](img/Screenshot_38.png)

This ATM Banking Application includes a web-based interface that provides terminal-like access to the Python application through a browser.

### Controller Layer (`controllers/default.js`)

The main controller handles the web interface and terminal integration.

#### Key Components:
- WebSocket Connection: real-time communication between the web client and the Python process.
- Child Process: uses Node’s child_process.spawn to run Python (`python -u run.py`) and pipe stdin/stdout/stderr.
- Credential Management: optionally writes creds.json from the CREDS environment variable at startup.

#### WebSocket Functionality:
- Process Spawning: each connection starts a new Python process in unbuffered mode (`-u`) with UTF-8 (`PYTHONIOENCODING=utf-8`).
- Real-time Output: Python stdout/stderr are forwarded to the browser as UTF-8 strings.
- Input Handling: browser keystrokes are sent over WebSocket and written to Python stdin (CR is normalized to LF for input()).
- Raw Mode: WebSocket runs in raw mode with encode/decode disabled to pass exact bytes when needed.

#### Data Flow:
1. Client opens WebSocket to the root path `/`.
2. Server spawns Python (`run.py`).
3. Server forwards Python output to client.
4. Client sends user input back to server; server writes it to Python stdin.
5. Server cleans up the process on disconnect.

#### Security Features:
- Automatic cleanup on disconnect.
- Optional credentials initialization from environment variables.
- No credentials are required to run in “demo mode” (when Google Sheets is unavailable).

### Views Layer (views/)
- layout.html
  - Base layout + xterm.js from CDN.
  - Global styles and background.
- index.html
  - Renders the “Run Program” button and terminal container.
  - Manually wires WebSocket and xterm (no attach addon) and implements a minimal “local echo” line editor:
    - Echoes typed characters locally.
    - Backspace support.
    - Sends the buffered line on Enter to Python input().

#### Customization tips
- Terminal size: change cols/rows in index.html Terminal({...}).
- Styles and background: edit CSS in layout.html.

### File Structure:
```
controllers/
  └── default.js     # WebSocket + child_process bridge to Python
views/
  ├── layout.html    # Base layout + xterm includes/styles
  └── index.html     # Terminal UI + manual WS wiring + local echo
run.py               # Python ATM app (Google Sheets optional)
index.js             # Total.js server entry
requirements.txt     # Python libs for Sheets integration
render.yaml          # Render deploy config
```

### Usage (Localhost)
1. Install Node 16+ and Python 3 on your PATH (verify: `python --version` or `python3 --version`).
2. Install Node deps:
   - `npm install`
3. Start the server:
   - `npm start`
4. Open http://localhost:3000
5. Click “Run Program”, click inside the terminal, type your input, and press Enter.
   - The browser provides local echo (characters appear as you type).
   - If Google Sheets isn’t configured, the app can still run in demo mode.

### Deploy on Render (Quick Guide)
1. Commit and push your repo with these files:
   - render.yaml
   - apt.txt
   - package.json
   - requirements.txt
   - index.js, controllers/default.js, views/*
2. Create a new Web Service on https://render.com/:
   - Select your Git repo.
   - Render auto-detects render.yaml.
3. Set environment variable:
   - CREDS = full JSON content of your Google service account (one-line or multiline).
   - Do NOT commit creds.json; rotate the key in GCP if it was committed.
4. Deploy:
   - Render installs Python (apt.txt), Python libs (requirements.txt), and Node deps (npm install).
   - The app will start on PORT provided by Render.
5. Open the service URL:
   - Click “Run Program”.
   - Type into the terminal; press Enter to submit.

Troubleshooting:
- Python not found: Ensure apt.txt exists with python3 and python3-pip.
- Google Sheets errors: The app still runs without Sheets; set CREDS to enable.
- Keyboard input: Click inside the terminal to focus; the client uses local echo and sends lines on Enter.

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
