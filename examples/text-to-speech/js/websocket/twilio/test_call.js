require('dotenv').config();
const twilio = require('twilio');

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const apiKeySid = process.env.TWILIO_API_KEY_SID;
const apiKeySecret = process.env.TWILIO_API_KEY_SECRET;

const client = twilio(apiKeySid, apiKeySecret, { accountSid });

const TO_NUMBER = process.env.TO_NUMBER;
const FROM_NUMBER = process.env.FROM_NUMBER;
const URL = process.env.NGROK_URL ? `${process.env.NGROK_URL}/voice` : 'http://localhost:3000/voice';

console.log(`Initiating call from ${FROM_NUMBER} to ${TO_NUMBER}`);
console.log(`Webhook URL: ${URL}`);

client.calls
  .create({
    url: URL,
    to: TO_NUMBER,
    from: FROM_NUMBER,
  })
  .then(call => console.log(`Call started: ${call.sid}`))
  .catch(err => console.error(`Error: ${err.message}`));
