const http = require('http');

let count = 0;

const server = http.createServer((req, res) => {
    count++;
    res.end(`Attendance count: ${count}`);
});

server.listen(3000, '0.0.0.0', () => {
    console.log("Server running");
});