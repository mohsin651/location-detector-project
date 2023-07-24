import streamlit as st
import speech_recognition as sr
import re
from pydub.playback import play
from pydub.generators import Sine
import pygame
import pyttsx3
import time

def play_startup_tone():
    pygame.mixer.init()
    pygame.mixer.music.load('sound.mp3')
    pygame.mixer.music.play()

# Create a function to play a sound
def beep():
    duration = 1000  # milliseconds
    frequency = 440  # Hz (A4)
    audio = Sine(frequency).to_audio_segment(duration=duration)
    play(audio)


def speak_message(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speech rate
    engine.setProperty('volume', 0.8)  # You can adjust the volume
    engine.say(message)
    engine.runAndWait()

def extract_coordinates(text):
    words = text.split()
    latitude = ""
    longitude = ""
    for word in words:
        if word.replace('.', '', 1).isdigit():  # Check if the word is a number
            if latitude == "":
                latitude = word
            else:
                longitude = word
                break  # Exit the loop after finding the second number
    
    return latitude, longitude

def main():
    st.title("Latitude and Longitude Detection")

    # Add a Start Recording button
    start_button = st.button("Start")

    play_startup_tone()
    time.sleep(2)
    # speak_message("Click the button below to start recording your location:")
    
    if start_button:
        speak_message("Now your voice is being recorded...")
        st.write("Recording...🔴")
        
        beep()

        # Record the user's voice using SpeechRecognition
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        beep()

        try:
            # Convert the recorded audio to text
            text = r.recognize_google(audio)
            st.write("You said: ", text)

            # Extract latitude and longitude from the text
            latitude, longitude = extract_coordinates(text)

            # Display latitude and longitude in input boxes
            lat_input = st.text_input("Latitude:", value=latitude if latitude is not None else "")
            lon_input = st.text_input("Longitude:", value=longitude if longitude is not None else "")

            # Update latitude and longitude if edited in the input boxes
            if lat_input:
                latitude = float(lat_input)
            if lon_input:
                longitude = float(lon_input)

            if latitude is not None and longitude is not None:
                st.success(f"Latitude: {latitude}, Longitude: {longitude}")
            else:
                st.warning("Latitude and Longitude could not be extracted. Please try again!")
            
            speak_message("Do you want to record again?, Yes or No")

            beep()
            with sr.Microphone() as source:
                audio = r.listen(source)
            beep()

            text = r.recognize_google(audio)

            if "yes" in text.lower():
                st.write("FFF")
                st.experimental_rerun()
            
            elif "no" in text.lower():
                speak_message("Thank You")
                pass

            else:
                speak_message("Thank You")
                pass

        except sr.UnknownValueError:
            st.error("Oops! The audio could not be understood. Please try again!")
        except sr.RequestError as e:
            st.error(f"Sorry, we encountered an error during the audio request: {e}")

if __name__ == "__main__":
    main()
