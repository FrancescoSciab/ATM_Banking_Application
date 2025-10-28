// Import required modules
const Pty = require('node-pty'); // Node.js library for spawning pseudo terminals
const fs = require('fs');        // File system module for file operations

/**
 * Install function to set up routes and websocket connections
 * This function is called when the controller is loaded
 */
exports.install = function () {
    // Set up the main route for the application
    ROUTE('/');
    
    // Set up websocket connection on root path with raw message handling
    WEBSOCKET('/', socket, ['raw']);
};

/**
 * WebSocket handler function for terminal connections
 * Manages the lifecycle of pseudo-terminal sessions for clients
 */
function socket() {
    // Disable automatic encoding/decoding of messages (handle raw data)
    this.encodedecode = false;
    
    // Enable automatic cleanup when connection closes
    this.autodestroy();

    /**
     * Handle new client connections
     * Creates a new pseudo-terminal for each client
     */
    this.on('open', function (client) {
        // Spawn a new pseudo-terminal running the Python ATM application
        client.tty = Pty.spawn('python3', ['run.py'], {
            name: 'xterm-color',    // Terminal type for color support
            cols: 80,               // Terminal width in columns
            rows: 24,               // Terminal height in rows
            cwd: process.env.PWD,   // Current working directory
            env: process.env        // Environment variables
        });

        /**
         * Handle terminal process exit
         * Cleans up resources when the Python process terminates
         */
        client.tty.on('exit', function (code, signal) {
            client.tty = null;      // Clear the terminal reference
            client.close();         // Close the websocket connection
            console.log("Process killed");
        });

        /**
         * Handle data output from the terminal
         * Forwards terminal output to the connected client
         */
        client.tty.on('data', function (data) {
            client.send(data);      // Send terminal output to websocket client
        });
    });

    /**
     * Handle client disconnection
     * Ensures proper cleanup of terminal processes when clients disconnect
     */
    this.on('close', function (client) {
        if (client.tty) {
            client.tty.kill(9);     // Force kill the terminal process (SIGKILL)
            client.tty = null;      // Clear the terminal reference
            console.log("Process killed and terminal unloaded");
        }
    });

    /**
     * Handle incoming messages from clients
     * Forwards user input from the web interface to the terminal
     */
    this.on('message', function (client, msg) {
        // Write the message to the terminal if it exists
        client.tty && client.tty.write(msg);
    });
}

/**
 * Initialize credentials file from environment variable
 * This runs when the module is loaded and creates the creds.json file
 * if the CREDS environment variable is set
 */
if (process.env.CREDS != null) {
    console.log("Creating creds.json file.");
    
    // Write the credentials from environment variable to creds.json file
    fs.writeFile('creds.json', process.env.CREDS, 'utf8', function (err) {
        if (err) {
            console.log('Error writing file: ', err);
            // Note: socket.emit won't work here as socket isn't defined in this scope
            socket.emit("console_output", "Error saving credentials: " + err);
        }
    });
}