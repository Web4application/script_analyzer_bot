import { analyzeTranscript } from './transcriptHandler.js';

if (message.startsWith('!analyze')) {
  const transcriptText = message.replace('!analyze', '').trim();
  const analysis = await analyzeTranscript(transcriptText);
  sendMessage(analysis); // Replace with your bot's response method
}
