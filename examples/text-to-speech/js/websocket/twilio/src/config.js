require('dotenv').config();

module.exports = {
  murfApiKey: process.env.MURF_API_KEY,
  twilioAccountSid: process.env.TWILIO_ACCOUNT_SID,
  twilioApiKeySid: process.env.TWILIO_API_KEY_SID,
  twilioApiKeySecret: process.env.TWILIO_API_KEY_SECRET,
  ngrokUrl: process.env.NGROK_URL,
  port: process.env.PORT || 3000,
  murfWsUrl: 'wss://global.api.murf.ai/v1/speech/stream-input',
  murfModel: 'FALCON',
  murfSampleRate: 8000,
  murfFormat: 'ULAW'
};
