import speech_recognition as sr
import os
from mtranslate import translate
from playsound import playsound
import threading

def translation_hin_to_eng(text):
    english_translation = translate(text, 'en-in')
    return english_translation

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 35000
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.5
    recognizer.pause_threshold = 0.5  # seconds of non-speaking audio before a phrase is considered complete
    recognizer.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
    recognizer.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    recognizer.non_speaking_duration = 0.4
    # Adjust this threshold based on your environment

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening....", end='', flush=True)
        try:
            audio = recognizer.listen(source, timeout=None)

            def rectext(audio):
                global translated_text# Pass 'audio' as an argument
                print("\rRecognizing...   ", end='', flush=True)
                recognized_text = recognizer.recognize_google(audio).lower()
                if recognized_text:
                    translated_text = translation_hin_to_eng(recognized_text)
                    print("\rMr.Stank: " + translated_text)
                    return translated_text

            play_sound_thread = threading.Thread(target=playsound, args=(r"F:\Python (First-Language)\Project\Jarvis\Data\mp3 data\wake.mp3",))
            rec_thread = threading.Thread(target=rectext, args=(audio,))  # Pass 'audio' as an argument
            play_sound_thread.start()
            rec_thread.start()

            play_sound_thread.join()
            rec_thread.join()
            return translated_text

        except sr.UnknownValueError:
            return ""  # Set recognized_text to an empty string in case of error
        finally:
            print("\r", end='', flush=True)  # Erase "Listening...." and "Recognizing..."
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console after recognition

def LISTEN():
    result = {"text": ""}  # Using a dictionary to store the result

    def store_result():
        result["text"] = listen()

    play_sound_thread = threading.Thread(target=playsound, args=(r"F:\Python (First-Language)\Project\Jarvis\Data\mp3 data\system_online_bleep.mp3",))
    listen_thread = threading.Thread(target=store_result)

    # Start both threads
    play_sound_thread.start()
    listen_thread.start()

    # Wait for both threads to finish
    play_sound_thread.join()
    listen_thread.join()

    return result["text"] or ""  # Return an empty string if result is None

LISTEN()