// Import required modules
// const Pty = require('node-pty'); // Node.js library for spawning pseudo terminals
const fs = require('fs');        // File system module for file operations
const path = require('path');    // Path utilities
const { spawn, spawnSync } = require('child_process'); // Use child_process instead of node-pty

/**
 * Install function to set up routes and websocket connections
 * This function is called when the controller is loaded
 */
exports.install = function () {
    // Render the index view
    ROUTE('/', function () {
        this.view('index');
    });

    // Use default websocket framing (text frames)
    WEBSOCKET('/', socket, ['raw']); // raw frames (no JSON encode/decode)
};

// Resolve a usable Python 3 binary across platforms
function resolvePython() {
    const candidates = [];
    if (process.env.PYTHON) candidates.push(process.env.PYTHON);
    if (process.env.PYTHON_BIN) candidates.push(process.env.PYTHON_BIN);

    const isWin = process.platform === 'win32';
    if (isWin) {
        candidates.push('python');
        candidates.push('python3');
        candidates.push('py -3');
        candidates.push('py');
    } else {
        candidates.push('python3');
        candidates.push('python');
    }

    const tried = [];
    for (const cand of candidates) {
        let cmd = cand;
        let args = [];
        if (cand.includes(' ')) {
            const parts = cand.split(' ').filter(Boolean);
            cmd = parts[0];
            args = parts.slice(1);
        }
        tried.push(cand);
        const res = spawnSync(cmd, [...args, '--version'], { encoding: 'utf8' });
        if (!res.error && res.status === 0) {
            return { cmd, args, tried };
        }
    }
    return { cmd: null, args: [], tried };
}

/**
 * WebSocket handler function for terminal connections
 * Manages the lifecycle of Python process sessions for clients
 */
function socket() {
    // Default encode/decode (JSON) prevents plain text input -> disable it
    this.encodedecode = false;
    // Enable automatic cleanup when connection closes
    this.autodestroy();

    this.on('open', function (client) {
        const scriptPath = path.join(__dirname, '..', 'run.py');

        // Resolve Python binary cross-platform
        const py = resolvePython();
        if (!py.cmd) {
            const msg = `Python 3 not found. Please install Python 3 and add it to PATH.
Tried: ${py.tried.join(', ')}
On Windows, install from python.org and ensure "Add python.exe to PATH" is selected.
`;
            client.send(msg.replace(/\n/g, '\r\n'));
            client.close();
            return;
        }

        // Use unbuffered mode (-u) and force UTF-8 encoding for stdout/stderr
        client.proc = spawn(py.cmd, [...py.args, '-u', scriptPath], {
            cwd: path.join(__dirname, '..'),
            env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
            stdio: ['pipe', 'pipe', 'pipe']
        });

        client.proc.on('error', (err) => {
            client.send(Buffer.from(`Failed to start Python: ${err.message}\r\n`, 'utf8'));
        });

        // Always send UTF-8 strings to the browser (avoid Buffer JSON)
        client.proc.stdout.on('data', (data) => client.send(data.toString('utf8')));
        client.proc.stderr.on('data', (data) => client.send(data.toString('utf8')));

        client.proc.on('close', () => {
            client.proc = null;
            try { client.close(); } catch {}
            console.log("Process killed");
        });
    });

    this.on('message', function (client, msg) {
        // msg is Buffer in raw mode; convert CR -> LF for Python input()
        if (client.proc?.stdin?.writable) {
            const buf = Buffer.isBuffer(msg) ? msg : Buffer.from(String(msg), 'utf8');
            const normalized = buf.toString('utf8').replace(/\r/g, '\n');
            client.proc.stdin.write(normalized);
        }
    });

    this.on('close', function (client) {
        if (client.proc) {
            try { client.proc.kill(); } catch {}
            client.proc = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    this.on('error', function (err) {
        console.error('WebSocket error:', err);
    });
}

/**
 * Initialize credentials file from environment variable
 * This runs when the module is loaded and creates the creds.json file
 * if the CREDS environment variable is set
 */
if (process.env.CREDS != null) {
    console.log("Creating creds.json file.");
    fs.writeFile('creds.json', process.env.CREDS, 'utf8', function (err) {
        if (err) {
            console.log('Error writing file: ', err);
        }
    });
}