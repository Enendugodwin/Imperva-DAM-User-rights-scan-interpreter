'use strict';

const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');

const pagePath = path.join(__dirname, 'index.html');
const server = http.createServer(async (request, response) => {
  const pathname = new URL(request.url, 'http://127.0.0.1').pathname;
  if (!['/', '/index.html'].includes(pathname)) {
    response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Not found');
    return;
  }
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.writeHead(405, { Allow: 'GET, HEAD' });
    response.end();
    return;
  }

  try {
    const html = await fs.readFile(pagePath);
    response.writeHead(200, {
      'Content-Type': 'text/html; charset=utf-8',
      'Content-Length': html.length,
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff'
    });
    response.end(request.method === 'HEAD' ? undefined : html);
  } catch {
    response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Could not read index.html');
  }
});

server.listen(8080, '127.0.0.1', () => {
  console.log('User Rights Scan web app: http://127.0.0.1:8080');
  console.log('Press Ctrl+C to stop the local server.');
});
