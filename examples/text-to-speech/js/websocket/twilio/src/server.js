const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const config = require('./config');
const TwilioService = require('./services/twilioService');

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/voice', (req, res) => {
  console.log('Incoming call received');
  
  const twiml = `
<Response>
  <Connect>
    <Stream url="wss://${req.headers.host}/streams" />
  </Connect>
</Response>
  `;

  res.type('text/xml');
  res.send(twiml);
});

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws, req) => {
  console.log('WebSocket connection established');
  
  if (req.url === '/streams') {
    const twilioService = new TwilioService(ws);
    
    ws.on('message', (message) => {
      twilioService.handleMessage(message);
    });
    
    ws.on('close', () => {
      console.log('WebSocket disconnected');
      twilioService.handleClose();
    });
  } else {
    ws.close();
  }
});

server.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`);
});
