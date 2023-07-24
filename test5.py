# 3j4rk3 -- Remove class approach

import streamlit as st
import speech_recognition as sr
from pydub.playback import play
from pydub.generators import Sine
import pygame
import pyttsx3
import time

class SoundPlayer:
    def __init__(self, sound_file):
        pygame.mixer.init()
        self.sound_file = sound_file

    def play_sound(self):
        pygame.mixer.music.load(self.sound_file)
        pygame.mixer.music.play()

class VoiceSynthesizer:
    def __init__(self, rate=150, volume=0.8):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak_message(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

class LocationRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record_audio(self, message="Now your voice is being recorded..."):
        with sr.Microphone() as source:
            self.audio = self.recognizer.listen(source)
        return self.recognizer.recognize_google(self.audio)

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

    start_button = st.button("Start")

    sound_player = SoundPlayer('sound.mp3')
    voice_synthesizer = VoiceSynthesizer()
    location_recorder = LocationRecorder()

    if start_button:
        sound_player.play_sound()
        time.sleep(2)

        voice_synthesizer.speak_message("Click the button below to start recording your location:")

        st.write("Recording...🔴")
        sound_player.play_sound()

        try:
            text = location_recorder.record_audio()
            st.write("You said:", text)

            latitude, longitude = extract_coordinates(text)

            lat_input = st.text_input("Latitude:", value=latitude if latitude is not None else "")
            lon_input = st.text_input("Longitude:", value=longitude if longitude is not None else "")

            if lat_input:
                latitude = float(lat_input)
            if lon_input:
                longitude = float(lon_input)

            if latitude is not None and longitude is not None:
                st.success(f"Latitude: {latitude}, Longitude: {longitude}")
            else:
                st.warning("Latitude and Longitude could not be extracted. Please try again!")

            voice_synthesizer.speak_message("Do you want to record again? Yes or No")
            sound_player.play_sound()

            text = location_recorder.record_audio()

            if "yes" in text.lower():
                st.experimental_rerun()
            elif "no" in text.lower():
                voice_synthesizer.speak_message("Thank You")
            else:
                voice_synthesizer.speak_message("Thank You")

        except sr.UnknownValueError:
            st.error("Oops! The audio could not be understood. Please try again!")
        except sr.RequestError as e:
            st.error(f"Sorry, we encountered an error during the audio request: {e}")

if __name__ == "__main__":
    main()
