// This code is from https://github.com/Azure-Samples/AzureSpeechReactSample in the src/App.js file
// There is also an example of text-to-speech that could be implemented

import { ResultReason } from 'microsoft-cognitiveservices-speech-sdk';

const sdk = require("microsoft-cognitiveservices-speech-sdk");

export async function transcribeFile(event) {
    return new Promise((resolve, reject) => {
        const audioFile = event.target.files[0];
        
        const speechConfig = sdk.SpeechConfig.fromSubscription(process.env.REACT_APP_SPEECH_KEY, process.env.REACT_APP_SPEECH_REGION);
        speechConfig.speechRecognitionLanguage = 'en-US';
        
        const audioConfig = sdk.AudioConfig.fromWavFileInput(audioFile);
        const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);
        
        recognizer.recognizeOnceAsync(result => {
            if (result.reason === ResultReason.RecognizedSpeech) {
                console.log(`RECOGNIZED: Text=${result.text}`);
                resolve(result.text);
            } else {
                console.log('ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.');
                reject('ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.');
            }
        });
    });
}

export async function sttFromMic() {
    const speechConfig = sdk.SpeechConfig.fromSubscription(process.env.REACT_APP_SPEECH_KEY, process.env.REACT_APP_SPEECH_REGION);
    speechConfig.speechRecognitionLanguage = 'en-US';
    
    const audioConfig = sdk.AudioConfig.fromDefaultMicrophoneInput();
    const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

    return new Promise((resolve, reject) => {
        recognizer.recognizeOnceAsync(result => {
            if (result.reason === ResultReason.RecognizedSpeech) {
                console.log(`RECOGNIZED: Text=${result.text}`);
                resolve(result.text);
            } else {
                console.log('ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.');
                reject('ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.');
            }
        });
    });
}

