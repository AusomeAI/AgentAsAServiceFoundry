// Minimal health-check server for the customer Console build (Doc 58 §7 /
// Doc 60's "a health-check endpoint the IaC's Container Apps configuration
// expects"). Deliberately stdlib-only, mirroring
// controlplane/shared/health.py's minimalism on the Python side — no
// framework is justified for one endpoint.
const http = require("http");

const server = http.createServer((req, res) => {
  if (req.url === "/healthz") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ service: "console-customer", status: "ok" }));
    return;
  }
  res.writeHead(404);
  res.end("not found");
});

server.listen(8080);
