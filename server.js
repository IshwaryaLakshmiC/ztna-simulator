#!/usr/bin/env node
/**
 * Local dev server for ZTNA Simulator
 * Serves index.html for all GET requests (SPA mode)
 * Usage: node server.js
 */
const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT = 8080;
const HTML = path.join(__dirname, 'index.html');

const server = http.createServer((req, res) => {
  // Serve index.html for every GET request
  // This means http://localhost:8080/, /index.html, /callback — all work
  if (req.method !== 'GET') {
    res.writeHead(405); res.end(); return;
  }

  fs.readFile(HTML, (err, data) => {
    if (err) {
      res.writeHead(500);
      res.end('Could not read index.html: ' + err.message);
      return;
    }
    res.writeHead(200, {
      'Content-Type':  'text/html; charset=utf-8',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma':        'no-cache',
    });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`\n  ZTNA Simulator running at http://localhost:${PORT}/`);
  console.log(`  Okta redirect URI to whitelist: http://localhost:${PORT}/\n`);
  console.log('  Ctrl+C to stop\n');
});
