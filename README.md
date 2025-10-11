# ATM Banking Application - Python

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
