require('total4'); // initializes global F

// Start HTTP server (auto-loads controllers and views)
F.http('release', { port: process.env.PORT || 3000 });
