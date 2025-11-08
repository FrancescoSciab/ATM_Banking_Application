# ATM Banking Application - Python

A web-based ATM banking simulation application built with Python and Node.js, featuring real-time terminal interaction through WebSocket connections.

## Live Demo
- **Production Site**: https://atm-banking-application.onrender.com/
- **Responsive Preview**: https://ui.dev/amiresponsive?url=https%3A%2F%2Fatm-banking-application.onrender.com%2F

![Responsive Preview](img/Amiresponsive.png)

## Table of Contents
- [ATM Banking Application - Python](#atm-banking-application---python)
  - [Live Demo](#live-demo)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Features](#features)
    - [Tech Stack](#tech-stack)
  - [ATM System Architecture](#atm-system-architecture)
    - [Understanding ATM Hardware](#understanding-atm-hardware)
    - [Software Components](#software-components)
    - [State Management](#state-management)
  - [Web Interface Architecture](#web-interface-architecture)
    - [Controller Layer](#controller-layer)
    - [Views Layer](#views-layer)
    - [File Structure](#file-structure)
  - [Installation & Setup](#installation--setup)
    - [Prerequisites](#prerequisites)
    - [Local Development](#local-development)
    - [Google Sheets Integration](#google-sheets-integration)
  - [Deployment](#deployment)
    - [Render Free Plan Setup](#render-free-plan-setup)
  - [Usage](#usage)
  - [Testing](#testing)
    - [Unit Testing](#unit-testing)
    - [Integration Testing](#integration-testing)
  - [Troubleshooting](#troubleshooting)
  - [Security](#security)
  - [Contributing](#contributing)

## Overview

This application simulates a real ATM banking system with a web-based terminal interface. It provides core banking functionalities including account authentication, balance checking, deposits, withdrawals, and transaction history.

### Features
- 🏧 **ATM Simulation**: Complete ATM workflow simulation
- 🔐 **Authentication**: Secure card number and PIN verification
- 💰 **Banking Operations**: Deposit, withdrawal, balance inquiry
- 📊 **Google Sheets Integration**: Real-time data storage and retrieval
- 🌐 **Web Terminal**: Browser-based terminal interface using xterm.js
- 🔄 **Real-time Updates**: WebSocket-powered live communication
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🛡️ **Security**: Encrypted credentials and secure data handling

### Tech Stack
- **Backend**: Python 3.x, Node.js with Total.js framework
- **Frontend**: HTML5, CSS3, JavaScript, xterm.js
- **Database**: Google Sheets API
- **Communication**: WebSocket for real-time terminal interaction
- **Deployment**: Render.com with automatic builds

[Back to Table of Contents](#table-of-contents)

## ATM System Architecture

### Understanding ATM Hardware

An ATM (Automated Teller Machine) consists of several key components:

#### Hardware Components
- **Card Reader**: Reads magnetic stripe or chip cards
- **PIN Pad**: Secure keypad for PIN entry and amount input
- **Display Screen**: Shows user interface (32x16 character grid traditionally)
- **Function Keys**: Side buttons (4+4) or touchscreen for menu navigation
- **Cash Dispenser**: Mechanical unit for dispensing banknotes
- **Receipt Printer**: Prints transaction receipts
- **Security Sensors**: Various sensors for tamper detection

#### Software Standards
The industry uses the **CEN/XFS** (eXtension For Financial Services) standard, which provides:
- Unified hardware abstraction layer
- Device driver standardization
- Client-server architecture with XFS Manager API

### Software Components

#### Banking Application Layer
The user-facing application that:
- Collects customer input
- Validates credentials
- Processes transactions
- Communicates with host systems
- Manages user interface flow

#### Communication Protocols
- **NDC/DDC**: Industry protocols for host communication
- **ISO 8583**: Message format for financial transactions
- **TLS/SSL**: Encrypted communication channels

### State Management

ATMs operate in different modes:
- **Power Up**: System initialization
- **Offline**: No server connection
- **Supervisor**: Service/maintenance mode
- **Out of Service**: Non-operational
- **In Service**: Normal operation mode

Each operational state (001-999) defines:
```
000 A001001011008004002001104
```
- `000`: State number
- `A`: State type (A=Card read, B=PIN entry, etc.)
- `001`: Screen number to display
- `001`: Success transition state
- `011`: Error transition state
- Additional parameters for specific operations

[Back to Table of Contents](#table-of-contents)

## Web Interface Architecture

![Screenshot 38](img/Screenshot_38.png)

### Controller Layer

**File**: `controllers/default.js`

Manages web interface and terminal integration with these key components:

#### WebSocket Connection
- Real-time bidirectional communication
- Handles multiple concurrent sessions
- Automatic connection recovery

#### Child Process Management
```javascript
// Spawns Python process with UTF-8 encoding
python = spawn('python', ['-u', 'run.py'], {
    env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
});
```

#### Features
- **Process Isolation**: Each connection gets its own Python instance
- **Real-time I/O**: Live stdout/stderr forwarding
- **Input Handling**: Browser keystrokes sent to Python stdin
- **Auto Cleanup**: Process termination on disconnect

### Views Layer

**Files**: `views/layout.html`, `views/index.html`

#### Layout Components
- **Base Template**: Common HTML structure and styling
- **xterm.js Integration**: Terminal emulator from CDN
- **Responsive Design**: Mobile-friendly interface

#### Terminal Features
- **Local Echo**: Immediate keystroke feedback
- **Line Editing**: Backspace support and input buffering
- **Enter Handling**: Sends complete lines to Python application

### File Structure
```
├── controllers/
│   └── default.js          # WebSocket + Python bridge
├── views/
│   ├── layout.html         # Base layout + xterm setup
│   └── index.html          # Terminal UI + WebSocket client
├── img/                    # Documentation images
├── run.py                  # Main Python ATM application
├── index.js                # Total.js server entry point
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── apt.txt                 # System packages for Render
└── README.md               # This documentation
```

[Back to Table of Contents](#table-of-contents)

## Installation & Setup

### Prerequisites
- **Node.js**: Version 20.x or higher
- **Python**: Version 3.8 or higher
- **Git**: For version control
- **Google Account**: For Sheets API (optional)

### Local Development

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd ATM_Banking_Application
```

2. **Install Node.js dependencies**:
```bash
npm install
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

4. **Start the development server**:
```bash
npm start
```

5. **Access the application**:
   - Open http://localhost:3000
   - Click "Run Program"
   - Follow the ATM prompts

### Google Sheets Integration

1. **Create Google Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google Sheets API
   - Create service account and download JSON key

2. **Setup Spreadsheet**:
   ```
   Spreadsheet Name: client_database
   Worksheet Name: client
   Headers: cardNum | pin | firstName | lastName | balance
   ```

3. **Share with Service Account**:
   - Share your spreadsheet with the service account email
   - Grant "Editor" permissions

4. **Configure Credentials** (Choose one method):
   
   **Method A: Environment Variable (Recommended)**
   ```bash
   export CREDS='{"type":"service_account","project_id":"..."}'
   ```
   
   **Method B: Local File**
   ```bash
   # Place your service account JSON as creds.json in project root
   cp path/to/your/service-account.json creds.json
   ```

[Back to Table of Contents](#table-of-contents)

## Deployment

### Render Free Plan Setup

1. **Prepare Repository**:
   - Ensure all files are committed to Git
   - Push to GitHub/GitLab

2. **Create Render Service**:
   - Visit [Render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your repository

3. **Configure Service**:
   ```
   Name: atm-banking-application
   Branch: main
   Runtime: Node
   Build Command: npm install && pip install -r requirements.txt
   Start Command: npm start
   ```

4. **Set Environment Variables**:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/creds.json
   ```

5. **Add Secret Files**:
   - File Name: `creds.json`
   - Content: Your complete Google service account JSON
   - Path: `/etc/secrets/creds.json`

![Secret file on Render](img/Secret-file-on-render.png)

6. **Select Instance Type**:
   - Choose "Free" for development/testing
   - Note: Free tier has 512MB RAM limit and cold starts

![Render Free plan selection](img/web-service-plan.png)

7. **Deploy**:
   - Click "Create Web Service"
   - Wait for build completion
   - Test your deployed application

[Back to Table of Contents](#table-of-contents)

## Usage

### Getting Started

1. **Access the Application**:
   - Navigate to your deployed URL or http://localhost:3000
   - Click "Run Program" button to start the ATM terminal

2. **Authentication Process**:
   ```
   ╔════════════════════════════════════════════════════════════════╗
   ║                         Welcome to the ATM                     ║
   ╚════════════════════════════════════════════════════════════════╝
   
   Insert Your Card: [Enter your 16-digit card number]
   PIN: [Enter your 4-digit PIN]
   ```

3. **ATM Main Menu**:
   After successful authentication, you'll see:
   ```
   ═══════════════════════════════════════════════════
                WELCOME TO YOUR ACCOUNT
   ═══════════════════════════════════════════════════
      Holder: [First Name] [Last Name]
      Card:   **** **** **** [Last 4 digits]
      Balance: €[Current Balance]
   ═══════════════════════════════════════════════════
      What would you like to do today?

   Please choose from one of the following options...
   1. Check Balance
   2. Withdraw Funds
   3. Deposit Funds
   4. Change PIN
   5. Transfer Money
   6. Exit
   ```

### Available Operations

#### 1. Check Balance 💰
- Displays your current account balance
- Real-time data from Google Sheets
- Shows balance in Euro (€) format with proper formatting

#### 2. Withdraw Funds 💸
- Enter amount to withdraw
- Automatic validation for:
  - Positive amounts only
  - Sufficient funds check
  - Real-time balance updates
- Format: Enter amount like `100` or `100.50`

#### 3. Deposit Funds 💵
- Enter amount to deposit
- Automatic validation for positive amounts
- Real-time balance updates
- Format: Enter amount like `50` or `75.25`

#### 4. Change PIN 🔐
- Enter new 4-digit PIN
- Confirm new PIN (must match)
- PIN must be numeric only
- Immediate database update

#### 5. Transfer Money 🔄
- **New Feature**: Send money to other cardholders
- Process:
  ```
  ==========================================
            MONEY TRANSFER
  ==========================================
  Amount to transfer: €[Enter amount]
  
  Enter recipient card number:
  → [Enter recipient's 16-digit card number]
  
  Send €[amount] to:
     [Recipient Name]
     Card: [Recipient Card Number]
  
  Confirm? (y/n): [y to confirm, n to cancel]
  
  SUCCESS! Transferred €[amount]
  To: [Recipient Name]
  Your new balance: €[New Balance]
  ```

#### 6. Exit 🚪
- Safely terminates the session
- Returns to main screen

### Test Card Holders

Use any of these sample accounts to test the application:

| Card Number      | PIN  | First Name | Last Name     | Features Available |
|------------------|------|------------|---------------|--------------------|
| 4532772818527395 | 1234 | Sergiy     | Kochenko      | All operations     |
| 4532761841325802 | 4321 | Oleg       | Dvoinisiuk    | All operations     |
| 5128381368581872 | 6543 | Francesco  | Sciabbarrasi  | All operations     |
| 6011188364697109 | 8765 | Brian      | McNamara      | All operations     |
| 490693153147110  | 2040 | Anna       | Watson        | All operations     |

### Sample Transaction Flow

**Complete ATM Session Example**:
```bash
# 1. Start Application
Insert Your Card: 4532772818527395
PIN: 1234

# 2. Welcome Screen
═══════════════════════════════════════════════════
             WELCOME TO YOUR ACCOUNT
═══════════════════════════════════════════════════
   Holder: Sergiy Kochenko
   Card:   **** **** **** 7395
   Balance: €1,250.75
═══════════════════════════════════════════════════

# 3. Check Balance
> 1
Current balance: €1,250.75

# 4. Withdraw Money
> 2
Amount to withdraw: 100
Withdrawn €100.00. New balance: €1,150.75

# 5. Transfer Money
> 5
Amount to transfer: €50
Enter recipient card number:
→ 4532761841325802

Send €50.00 to:
   Oleg Dvoinisiuk
   Card: 4532761841325802

Confirm? (y/n): y

SUCCESS! Transferred €50.00
To: Oleg Dvoinisiuk
Your new balance: €1,100.75

# 6. Exit
> 6
Goodbye!
```

### Input Formats

**Amounts**: 
- Accepts: `100`, `100.50`, `100,50`, `1 250,75`
- Automatically converts European format (comma as decimal)
- Must be positive numbers

**Card Numbers**: 
- 16-digit format
- No spaces or dashes required
- Example: `4532772818527395`

**PIN**: 
- 4-digit numeric code
- No spaces allowed
- Example: `1234`

### Error Handling

The application includes comprehensive error handling for:

- **Invalid Card**: "Card not found"
- **Wrong PIN**: "Incorrect PIN" (max 3 attempts)
- **Insufficient Funds**: "Withdrawal failed (insufficient funds)"
- **Invalid Amount**: "Invalid amount" or "Amount must be positive"
- **Transfer Errors**: "Recipient card not found" or "You cannot transfer to yourself"
- **Server Errors**: "Failed to update database" or "Server connection error"

### Security Features

- **Session Isolation**: Each user gets a separate Python process
- **PIN Verification**: Secure PIN validation with attempt limits
- **Input Validation**: All inputs are sanitized and validated
- **Real-time Updates**: Immediate database synchronization
- **Transfer Confirmation**: Double confirmation for money transfers

> **Note**: This is a demonstration application. All test accounts are for educational purposes only. In production, additional security measures including encryption, audit logging, and regulatory compliance would be required.

[Back to Table of Contents](#table-of-contents)

## Testing

### Unit Testing

Create comprehensive unit tests for core functionality:

```python
# unittest.py
import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestATMFunctionality(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def test_card_validation(self):
        """Test card number validation."""
        pass
    
    def test_pin_verification(self):
        """Test PIN verification logic."""
        pass
    
    def test_balance_inquiry(self):
        """Test balance checking functionality."""
        pass
    
    def test_withdrawal_limits(self):
        """Test withdrawal amount validation."""
        pass
    
    def test_deposit_validation(self):
        """Test deposit amount validation."""
        pass

if __name__ == '__main__':
    unittest.main()
```

**Run tests**:
```bash
python unittest.py
```

### Integration Testing

Test the complete workflow:

1. **Web Interface Testing**:
   - Terminal connection establishment
   - WebSocket communication
   - User input handling

2. **Google Sheets Integration**:
   - Authentication verification
   - Data retrieval accuracy
   - Update operations

3. **End-to-End Testing**:
   - Complete ATM transaction flows
   - Error handling scenarios
   - Session management

[Back to Table of Contents](#table-of-contents)

## Troubleshooting

### Common Issues

**Card Not Found**:
- ✅ Verify spreadsheet name: `client_database`
- ✅ Check worksheet name: `client`
- ✅ Ensure headers: `cardNum | pin | firstName | lastName | balance`
- ✅ Share sheet with service account email
- ✅ Check Google Cloud Console for API quotas

**Authentication Errors**:
- ✅ Verify service account JSON format
- ✅ Check file permissions on creds.json
- ✅ Ensure Google Sheets API is enabled
- ✅ Validate environment variable setup

**Terminal Issues**:
- ✅ Click inside terminal area to focus
- ✅ Press Enter to submit input lines
- ✅ Clear browser cache if display issues occur
- ✅ Check browser console for JavaScript errors

**Render Deployment Issues**:
- ✅ Verify Node.js version in package.json
- ✅ Check build logs for errors
- ✅ Ensure all dependencies are listed
- ✅ Validate secret file configuration

**Performance Issues (Free Tier)**:
- ✅ Cold starts can take 30-60 seconds
- ✅ Service sleeps after 15 minutes of inactivity
- ✅ Memory limit: 512MB (monitor usage)

### Getting Help

If you encounter issues:

1. Check the Render logs:
   ```bash
   # View recent logs
   render logs --tail=100
   ```

2. Test locally first:
   ```bash
   npm start
   ```

3. Verify Google Sheets manually:
   - Open your spreadsheet
   - Check data format
   - Verify sharing permissions

[Back to Table of Contents](#table-of-contents)

## Security

### Best Practices

- 🔐 **Never commit credentials**: Use `.gitignore` for sensitive files
- 🔑 **Use environment variables**: Store secrets securely
- 🛡️ **Rotate keys regularly**: Update service account keys periodically
- 🔒 **Limit permissions**: Grant minimum required access
- 🚫 **Validate inputs**: Sanitize all user inputs
- 🔍 **Monitor access**: Review Google Cloud audit logs

### Security Features

- **Encrypted communication**: All data transmitted over HTTPS/WSS
- **Process isolation**: Each session runs in separate Python process
- **Credential management**: Secure handling of authentication tokens
- **Input validation**: Protection against injection attacks

[Back to Table of Contents](#table-of-contents)

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request`

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write tests for new features
- Update documentation for changes
- Test both locally and on Render

[Back to Table of Contents](#table-of-contents)

## Acknowledgments

We would like to express our sincere gratitude to the following individuals and institutions who made this project possible:

### Academic Institution
- **[Atlantic Technological University (ATU)](https://www.atu.ie/)** - BSc Honours in Contemporary Software Development Program
- **ATU Donegal Campus** - For providing comprehensive support to our development team and offering individual assistance throughout all phases of the project

### Educational Support
- **ATU Donegal Tutor Support Team** - For their dedicated guidance and technical assistance
- **Lusungu Mwasinga** - Our course instructor, for exceptional teaching and mentorship throughout the development process

### Development Team
Special thanks to our collaborative development team members who contributed to building this ATM Banking Application:

- **Sergiy Kochenko** - Lead Developer & Project Coordinator
- **[Team Member 2]** - [Role/Contribution]
- **[Team Member 3]** - [Role/Contribution] 
- **[Team Member 4]** - [Role/Contribution]

### Technical Acknowledgments
- **Google Cloud Platform** - For providing the Sheets API infrastructure
- **Render.com** - For reliable hosting and deployment services
- **Total.js Framework** - For the web application framework
- **xterm.js** - For the terminal emulation library

### Open Source Community
This project builds upon the excellent work of the open-source community. We acknowledge all the developers and contributors whose libraries and frameworks made this application possible.

---

## Note
This application is for educational purposes and demonstrates ATM system concepts. For production banking applications, additional security measures, compliance requirements, and regulatory approvals would be necessary.

[Back to Table of Contents](#table-of-contents)
