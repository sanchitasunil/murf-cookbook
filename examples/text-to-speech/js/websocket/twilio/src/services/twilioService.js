const MurfService = require('./murfService');

class TwilioService {
  constructor(ws) {
    this.ws = ws;
    this.streamSid = null;
    this.murfReady = false;
    this.greetingSent = false;
    
    this.murfService = new MurfService({
      onOpen: () => {
        console.log('Murf ready');
        this.murfReady = true;
        this.sendGreetingIfReady();
      },
      onAudio: (base64Audio) => {
        this.sendAudioToTwilio(base64Audio);
      },
      onError: (err) => {
        console.error('Murf error:', err);
      },
      onClose: () => {
        console.log('Murf closed');
      }
    });

    this.murfService.connect();
  }

  sendGreetingIfReady() {
    if (this.murfReady && this.streamSid && !this.greetingSent) {
      console.log('Sending greeting');
      this.murfService.sendText("Hello! This is a test of Murf integration with Twilio. The quick brown fox jumps over the lazy dog.");
      this.greetingSent = true;
    }
  }

  handleMessage(message) {
    try {
      const msg = JSON.parse(message);
      
      switch (msg.event) {
        case 'start':
          this.streamSid = msg.start.streamSid;
          console.log(`Media stream started: ${this.streamSid}`);
          this.sendGreetingIfReady();
          break;
          
        case 'media':
          break;
          
        case 'stop':
          console.log('Media stream stopped');
          this.murfService.disconnect();
          break;
          
        case 'connected':
          console.log('Media stream connected');
          break;

        default:
          console.log('Unknown event:', msg.event);
      }
    } catch (error) {
      console.error('Error handling message:', error);
    }
  }

  sendAudioToTwilio(base64Audio) {
    if (!this.streamSid) {
      console.warn('StreamSID not established');
      return;
    }

    const mediaMessage = {
      event: 'media',
      streamSid: this.streamSid,
      media: {
        payload: base64Audio
      }
    };

    if (this.ws.readyState === 1) {
      this.ws.send(JSON.stringify(mediaMessage));
    }
  }
  
  handleClose() {
    this.murfService.disconnect();
  }
}

module.exports = TwilioService;
