const WebSocket = require('ws');
const config = require('../config');

class MurfService {
  constructor(callbacks) {
    this.ws = null;
    this.callbacks = callbacks || {};
    this.isConnected = false;
  }

  connect() {
    const url = `${config.murfWsUrl}?api_key=${config.murfApiKey}&model=${config.murfModel}&sample_rate=${config.murfSampleRate}&format=${config.murfFormat}`;
    
    console.log('Connecting to Murf TTS WebSocket');
    this.ws = new WebSocket(url);

    this.ws.on('open', () => {
      console.log('Murf WebSocket connected');
      this.isConnected = true;
      if (this.callbacks.onOpen) this.callbacks.onOpen();
    });

    this.ws.on('message', (data) => {
      try {
        const message = JSON.parse(data);
        
        if (message.audio) {
          if (this.callbacks.onAudio) {
            this.callbacks.onAudio(message.audio);
          }
        } else if (message.error) {
          console.error('Murf error:', message.error);
        }
      } catch (error) {
        console.error('Error parsing Murf message:', error);
      }
    });

    this.ws.on('error', (error) => {
      console.error('Murf WebSocket error:', error);
      if (this.callbacks.onError) this.callbacks.onError(error);
    });

    this.ws.on('close', (code, reason) => {
      console.log('Murf WebSocket closed');
      this.isConnected = false;
      if (this.callbacks.onClose) this.callbacks.onClose(code, reason);
    });
  }

  sendText(text, contextId = null) {
    if (!this.isConnected) {
      console.warn('Murf WebSocket not connected');
      return;
    }

    const payload = {
      text: text,
      format: config.murfFormat,
      voice_config: {
        voiceId: 'Matthew',
        style: 'Conversational'
      },
      end: true
    };

    if (contextId) {
      payload.context_id = contextId;
    }

    console.log('Sending text to Murf:', text);
    this.ws.send(JSON.stringify(payload));
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

module.exports = MurfService;
