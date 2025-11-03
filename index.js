require('total4'); // initializes global F

// Start HTTP server (auto-loads controllers and views)
// Bind to localhost in dev (no PORT), otherwise 0.0.0.0 for hosting platforms
const port = Number(process.env.PORT || 3000);
const ip = process.env.PORT ? '0.0.0.0' : 'localhost';
F.http('release', { port, ip });
