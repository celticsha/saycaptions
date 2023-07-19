# saycaptions
Quick and effective way to caption folder of images using voice.

There are many effective AI tools for writing captions for images, but sometimes you want to use your own words, escpecially for training your own models. For many, speaking is faster than typing. Using a cloud speech to text system, in this case Google Cloud Speech, allows you guide the recognition to favour words that are likely to come up in your images, thus improving accuracy. 

## Set up

### Installation

You need:
- speech_recognition
- pyaudio
- cv2
- google-cloud-speech

You need a service key (json file) for Google Cloud Speech - https://cloud.google.com/speech-to-text/docs/before-you-begin

Note: you can use recognize_google (instead of recognize_google_cloud) for free without an API key, but that doesn't allow you to setup preferred phases. This extra layer of customisation helps with accuracy thus impoving speed.

### Customisation

In caption.py

1. Point the code to the folder containing the png images you wish to caption.
2. Point GOOGLE_CLOUD_SPEECH_CREDENTIALS at your service key
3. Set the language code (see https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages)
4. Change the screen resolution variable to adjust where your image previews appear

You may wish to edit phrases.txt to suit your use case.

## Usage
- Run caption.py
- A preview of an image that needs a caption is displayed
- Press any key to start recording
- Stop speaking to stop recording
- A transcript appears on screen for you to approve, retry or append
- If approved, a text file with the same name as the image is created containing the caption
- Continues cycling through the png images until all have captions

## Known Issues
### RecognitionConfig Fix
If you see "ValueError: Unknown field for RecognitionConfig: speechContexts"
Look for the file __ini__.py in site_packages/speech_recognition

Change
```
 if preferred_phrases is not None:
            config['speechContexts'] = [speech.SpeechContext(
                phrases=preferred_phrases
            )]
```
to
```
 if preferred_phrases is not None:
            config['speech_contexts'] = [speech.SpeechContext(
                phrases=preferred_phrases
            )]
```      
Tested on Windows only.
