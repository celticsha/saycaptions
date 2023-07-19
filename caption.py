import os
import speech_recognition as sr
import cv2
import time
import sys
import random

# point to the folder containing your image png files. txt files with the same names will be created containing the captions.
image_path = "[your image path]"

# the json credentials you downloaded from Google
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"[your json file]"

# set screen width to preview image on the right (position your console window on the left for ease of use)
screen_w=1280

#the number of seconds the recogniser detects as a long enough pause to infer the end of a caption
pause_threshold=1

#chose the appropriate language code for your language and dialect - see https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
lang="en-GB"

# a text file containing phrases that you are likely to use in captioning
with open('phrases.txt') as f:
	phrase_hints = f.read().splitlines()
         

x=int(screen_w/2)



def transcribe_voice_memo(existing):
    recognizer = sr.Recognizer()
    recognizer.recognize_google_cloud
    recognizer.pause_threshold = pause_threshold
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source,duration=0.1)
        print("Please speak your caption.")
        if c==0:
        	print("Recording will end automatically.")
        audio_data = recognizer.listen(source)
        try: 
            transcription = recognizer.recognize_google_cloud(audio_data, language=lang, show_all=False, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, preferred_phrases=phrase_hints) 
            if existing !="":
            	transcription=existing+", "+transcription
            print("\n\""+transcription+"\"\n")
            return transcription
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print("Error with the speech recognition service; {0}".format(e))
    return None

def save_transcription(image_path, transcription):
    directory, filename = os.path.split(image_path)
    file_extension = os.path.splitext(filename)[1]
    text_filename = os.path.splitext(filename)[0] + ".txt"
    text_path = os.path.join(directory, text_filename)
    with open(text_path, "w") as file:
        file.write(transcription)


all_files=os.listdir(image_path)
files=[]
image_count=0
caption_count=0
for file_name in all_files:
	split_tup = os.path.splitext(file_name)
	if split_tup[1]!=".png":
		continue
	image_count+=1
	image_file=image_path+"/"+file_name
	text_file=image_file.replace(".png",".txt")
	if os.path.isfile(text_file):
		caption_count+=1
		continue
	files.append(file_name)
	
# shuffling helps keep similar images fresh in your mind
random.shuffle(files)
	
print("Images found: "+str(image_count))
print("Images with captions already: "+str(caption_count))
print("Images needing captions: "+str(image_count-caption_count)+"\n")
	
c=0
existing=""
while files:
	file_name=files.pop(0)	
	image_file=image_path+"/"+file_name
	image = cv2.imread(image_file)
	h, w = image.shape[:2]	
	cv2.namedWindow('Window', cv2.WINDOW_KEEPRATIO)
	cv2.moveWindow('Window', x, 0)
	cv2.imshow("Window", image)
	cv2.resizeWindow('Window', x, x)
	
	if existing=="":
		print("Press any key when you're ready to record your next caption.")
	else:
		print("Press any key when you're ready to record the rest of your caption.")
	cv2.waitKey()
	
	transcription = transcribe_voice_memo(existing)
	cv2.destroyAllWindows()
	if transcription:
			user_input = input("Are you happy with this caption? 'Y'/'N' or 'A' to append:")
			if user_input.lower()=="y":
				print("Caption saved successfully. "+str(len(files))+" to go.\n")
				save_transcription(image_file, transcription)
				existing=""
			elif user_input.lower()=="a":
				print("Great. You can add to that caption.")
				files.insert(0, file_name)
				existing=transcription
			elif user_input.lower()=="q":
				print("Bye")
				sys.exit()
			else:
				print("\nOkay. Let's have another go at that one.\n")
				files.insert(0, file_name)
				existing=""
	else:
	    print("Transcription failed. Let's try again\n")
	    files.insert(0, file_name)
	c=c+1
	
print("Text files created for all images in chosen directory.")