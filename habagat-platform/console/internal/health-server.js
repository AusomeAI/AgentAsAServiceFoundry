// Minimal health-check server for the internal-operator Console build —
// see console/customer/health-server.js for the identical rationale.
const http = require("http");

const server = http.createServer((req, res) => {
  if (req.url === "/healthz") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ service: "console-internal", status: "ok" }));
    return;
  }
  res.writeHead(404);
  res.end("not found");
});

server.listen(8080);
